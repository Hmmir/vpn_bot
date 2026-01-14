from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
import sqlite3
from typing import Iterable, List


BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "bot.db"


@dataclass(frozen=True)
class Reminder:
    user_id: int
    lang: str
    kind: str


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _connect() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with _connect() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                lang TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS subscriptions (
                user_id INTEGER PRIMARY KEY,
                plan_code TEXT,
                expires_at TEXT,
                status TEXT NOT NULL,
                reminded_3d INTEGER NOT NULL DEFAULT 0,
                reminded_1d INTEGER NOT NULL DEFAULT 0,
                reminded_0d INTEGER NOT NULL DEFAULT 0,
                reminded_expired INTEGER NOT NULL DEFAULT 0,
                updated_at TEXT NOT NULL,
                FOREIGN KEY(user_id) REFERENCES users(user_id)
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS user_keys (
                user_id INTEGER PRIMARY KEY,
                vless_uri TEXT,
                sub_url TEXT,
                client_id TEXT,
                email TEXT,
                sub_id TEXT,
                updated_at TEXT NOT NULL,
                FOREIGN KEY(user_id) REFERENCES users(user_id)
            )
            """
        )


def upsert_user(user_id: int, lang: str) -> None:
    now = _now_iso()
    with _connect() as conn:
        conn.execute(
            """
            INSERT OR IGNORE INTO users (user_id, lang, created_at, updated_at)
            VALUES (?, ?, ?, ?)
            """,
            (user_id, lang, now, now),
        )
        conn.execute(
            """
            UPDATE users SET lang = ?, updated_at = ? WHERE user_id = ?
            """,
            (lang, now, user_id),
        )


def set_subscription(user_id: int, expires_at_iso: str, plan_code: str = "manual") -> None:
    now = _now_iso()
    with _connect() as conn:
        conn.execute(
            """
            INSERT INTO subscriptions (
                user_id, plan_code, expires_at, status,
                reminded_3d, reminded_1d, reminded_0d, reminded_expired, updated_at
            )
            VALUES (?, ?, ?, 'active', 0, 0, 0, 0, ?)
            ON CONFLICT(user_id) DO UPDATE SET
                plan_code = excluded.plan_code,
                expires_at = excluded.expires_at,
                status = 'active',
                reminded_3d = 0,
                reminded_1d = 0,
                reminded_0d = 0,
                reminded_expired = 0,
                updated_at = excluded.updated_at
            """,
            (user_id, plan_code, expires_at_iso, now),
        )


def mark_reminded(user_id: int, kind: str) -> None:
    field_map = {
        "3d": "reminded_3d",
        "1d": "reminded_1d",
        "0d": "reminded_0d",
        "expired": "reminded_expired",
    }
    field = field_map.get(kind)
    if not field:
        return
    with _connect() as conn:
        conn.execute(
            f"UPDATE subscriptions SET {field} = 1, updated_at = ? WHERE user_id = ?",
            (_now_iso(), user_id),
        )


def set_status_expired(user_id: int) -> None:
    with _connect() as conn:
        conn.execute(
            "UPDATE subscriptions SET status = 'expired', updated_at = ? WHERE user_id = ?",
            (_now_iso(), user_id),
        )


def set_user_key(
    user_id: int,
    vless_uri: str,
    sub_url: str,
    client_id: str = "",
    email: str = "",
    sub_id: str = "",
) -> None:
    with _connect() as conn:
        conn.execute(
            """
            INSERT INTO user_keys (user_id, vless_uri, sub_url, client_id, email, sub_id, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(user_id) DO UPDATE SET
                vless_uri = excluded.vless_uri,
                sub_url = excluded.sub_url,
                client_id = excluded.client_id,
                email = excluded.email,
                sub_id = excluded.sub_id,
                updated_at = excluded.updated_at
            """,
            (user_id, vless_uri, sub_url, client_id, email, sub_id, _now_iso()),
        )


def get_user_key(user_id: int) -> tuple[str, str]:
    with _connect() as conn:
        row = conn.execute(
            "SELECT vless_uri, sub_url FROM user_keys WHERE user_id = ?",
            (user_id,),
        ).fetchone()
    if not row:
        return "", ""
    return row["vless_uri"] or "", row["sub_url"] or ""


def list_due_reminders(now: datetime) -> List[Reminder]:
    reminders: List[Reminder] = []
    with _connect() as conn:
        rows = conn.execute(
            """
            SELECT s.*, u.lang
            FROM subscriptions s
            JOIN users u ON u.user_id = s.user_id
            WHERE s.expires_at IS NOT NULL
            """
        ).fetchall()
    for row in rows:
        expires_at = datetime.fromisoformat(row["expires_at"])
        delta = expires_at - now
        seconds = delta.total_seconds()
        if seconds <= 0:
            if not row["reminded_expired"]:
                reminders.append(Reminder(row["user_id"], row["lang"], "expired"))
            continue
        if seconds <= 24 * 3600:
            if not row["reminded_1d"]:
                reminders.append(Reminder(row["user_id"], row["lang"], "1d"))
            continue
        if seconds <= 3 * 24 * 3600:
            if not row["reminded_3d"]:
                reminders.append(Reminder(row["user_id"], row["lang"], "3d"))
    return reminders
