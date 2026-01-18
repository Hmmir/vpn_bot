from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
import uuid
from typing import Optional

import logging

from .config import (
    XUI_BASE_URL,
    XUI_USERNAME,
    XUI_PASSWORD,
    XUI_API_PATH,
    XUI_INBOUND_IDS,
    XUI_INBOUND_ID,
    XUI_FLOW,
    XUI_TOTAL_GB,
    XUI_LIMIT_IP,
    XUI_PUBLIC_HOST,
    XUI_PUBLIC_PORT,
    XUI_SUB_BASE_URL,
    XUI_SSL_VERIFY,
)
from .data import PLAN_DAYS
from .storage import set_subscription, set_user_key
from .xui_api import XuiApi, XuiInbound, XuiKey, build_sub_url, build_vless_uri


_xui_client: Optional[XuiApi] = None


def _parse_inbound_id(value: str) -> Optional[int]:
    return int(value) if value.strip().isdigit() else None


def _parse_inbound_ids() -> list[int]:
    ids: list[int] = []
    raw = XUI_INBOUND_IDS.strip()
    if raw:
        for part in raw.split(","):
            value = part.strip()
            if value.isdigit():
                ids.append(int(value))
    if not ids:
        inbound_id = _parse_inbound_id(XUI_INBOUND_ID)
        if inbound_id is not None:
            ids.append(inbound_id)
    seen: set[int] = set()
    result: list[int] = []
    for inbound_id in ids:
        if inbound_id in seen:
            continue
        seen.add(inbound_id)
        result.append(inbound_id)
    return result


def _public_port() -> Optional[int]:
    if not XUI_PUBLIC_PORT:
        return None
    if XUI_PUBLIC_PORT.strip().isdigit():
        return int(XUI_PUBLIC_PORT.strip())
    return None


def _public_host() -> str:
    if XUI_PUBLIC_HOST:
        return XUI_PUBLIC_HOST
    if XUI_BASE_URL.startswith("http"):
        return XUI_BASE_URL.split("://", 1)[1].split(":", 1)[0]
    return ""


async def ensure_xui() -> Optional[XuiApi]:
    global _xui_client
    if _xui_client:
        return _xui_client
    if not (XUI_BASE_URL and XUI_USERNAME and XUI_PASSWORD):
        return None
    _xui_client = XuiApi(
        XUI_BASE_URL,
        XUI_USERNAME,
        XUI_PASSWORD,
        api_path=XUI_API_PATH or "/panel/api",
        verify_ssl=XUI_SSL_VERIFY,
    )
    return _xui_client


def _find_existing_client(clients: list[dict], user_id: int) -> Optional[dict]:
    target_email = f"tg_{user_id}"
    for client in clients:
        if client.get("email") == target_email:
            return client
        if str(client.get("tgId", "")) == str(user_id):
            return client
    return None


async def list_inbounds() -> list[dict]:
    xui = await ensure_xui()
    if not xui:
        return []
    return await xui.list_inbounds()


async def issue_access(user_id: int, plan_code: str) -> XuiKey:
    days = PLAN_DAYS.get(plan_code)
    if not days:
        raise RuntimeError("Invalid plan code")

    inbound_ids = _parse_inbound_ids()
    if not inbound_ids:
        raise RuntimeError("XUI_INBOUND_ID/XUI_INBOUND_IDS is missing")

    xui = await ensure_xui()
    if not xui:
        raise RuntimeError("XUI is not configured")

    inbound_rows: list[tuple[int, XuiInbound]] = []
    for inbound_id in inbound_ids:
        inbound = await xui.get_inbound(inbound_id)
        if inbound:
            inbound_rows.append((inbound_id, inbound))
        else:
            logging.warning("Inbound %s not found", inbound_id)
    if not inbound_rows:
        raise RuntimeError("No valid inbounds found")

    existing = None
    for _, inbound in inbound_rows:
        existing = _find_existing_client(inbound.clients, user_id)
        if existing:
            break
    expires = datetime.now(timezone.utc) + timedelta(days=days)
    expiry_ms = int(expires.timestamp() * 1000)

    primary_client_id = existing.get("id") if existing else str(uuid.uuid4())
    email = existing.get("email") if existing else f"tg_{user_id}"
    sub_id = existing.get("subId") if existing else uuid.uuid4().hex[:16]
    flow = XUI_FLOW or (existing.get("flow") if existing else "")
    settings = {
        "id": primary_client_id,
        "email": email,
        "limitIp": XUI_LIMIT_IP,
        "totalGB": XUI_TOTAL_GB,
        "expiryTime": expiry_ms,
        "enable": True,
        "flow": flow or None,
        "tgId": str(user_id),
        "subId": sub_id,
    }
    settings = {k: v for k, v in settings.items() if v is not None}

    for inbound_id, inbound in inbound_rows:
        existing_inbound = _find_existing_client(inbound.clients, user_id)
        client_id = existing_inbound.get("id") if existing_inbound else primary_client_id
        payload = dict(settings)
        payload["id"] = client_id
        if existing_inbound:
            update_id = existing_inbound.get("id") or client_id
            result = await xui.update_client(update_id, inbound_id, payload)
        else:
            result = await xui.add_client(inbound_id, payload)
        if not result.get("success"):
            raise RuntimeError(f"XUI error: {result}")

    host = _public_host()
    port = _public_port()
    primary_inbound = inbound_rows[0][1]
    vless_uri = build_vless_uri(
        primary_inbound,
        primary_client_id,
        email,
        host=host,
        flow=flow,
        public_port=port,
    )
    sub_base = XUI_SUB_BASE_URL or XUI_BASE_URL
    sub_url = build_sub_url(sub_base, sub_id)
    set_user_key(user_id, vless_uri, sub_url, primary_client_id, email, sub_id)
    set_subscription(user_id, expires.isoformat(timespec="seconds"), plan_code=plan_code)
    return XuiKey(vless_uri=vless_uri, sub_url=sub_url, client_id=primary_client_id, email=email, sub_id=sub_id)
