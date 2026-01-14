from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Optional
from urllib.parse import urlencode, quote

import aiohttp


@dataclass(frozen=True)
class XuiInbound:
    raw: dict[str, Any]

    @property
    def port(self) -> int:
        return int(self.raw.get("port", 0) or 0)

    @property
    def protocol(self) -> str:
        return self.raw.get("protocol", "")

    @property
    def stream_settings(self) -> dict[str, Any]:
        raw = self.raw.get("streamSettings") or {}
        if isinstance(raw, str):
            try:
                return json.loads(raw)
            except json.JSONDecodeError:
                return {}
        return raw


@dataclass(frozen=True)
class XuiKey:
    vless_uri: str
    sub_url: str
    client_id: str
    email: str
    sub_id: str


class XuiApi:
    def __init__(
        self,
        base_url: str,
        username: str,
        password: str,
        api_path: str = "/panel/api",
        verify_ssl: bool = True,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.username = username
        self.password = password
        self.api_path = api_path.rstrip("/")
        self._session = aiohttp.ClientSession(
            cookie_jar=aiohttp.CookieJar(unsafe=True),
            connector=aiohttp.TCPConnector(ssl=verify_ssl),
        )
        self._logged_in = False

    async def close(self) -> None:
        await self._session.close()

    async def _login(self) -> None:
        url = f"{self.base_url}/login"
        payload = {"username": self.username, "password": self.password}
        async with self._session.post(url, data=payload) as resp:
            data = await resp.json(content_type=None)
        if not data.get("success"):
            raise RuntimeError(f"XUI login failed: {data}")
        self._logged_in = True

    async def _request(self, method: str, path: str, json_body: Any | None = None) -> dict:
        if not self._logged_in:
            await self._login()
        url = f"{self.base_url}{self.api_path}{path}"
        async with self._session.request(method, url, json=json_body) as resp:
            if resp.status == 401:
                self._logged_in = False
                await self._login()
                async with self._session.request(method, url, json=json_body) as retry:
                    return await retry.json(content_type=None)
            return await resp.json(content_type=None)

    async def list_inbounds(self) -> list[dict[str, Any]]:
        data = await self._request("GET", "/inbounds/list")
        return data.get("obj", []) if isinstance(data, dict) else []

    async def get_inbound(self, inbound_id: int) -> Optional[XuiInbound]:
        data = await self._request("GET", f"/inbounds/get/{inbound_id}")
        inbound = data.get("obj") if isinstance(data, dict) else None
        return XuiInbound(inbound) if inbound else None

    async def add_client(self, inbound_id: int, client_settings: dict[str, Any]) -> dict:
        payload = {
            "id": inbound_id,
            "settings": json.dumps({"clients": [client_settings]}),
        }
        return await self._request("POST", "/inbounds/addClient", payload)


def build_vless_uri(
    inbound: XuiInbound,
    client_id: str,
    email: str,
    host: str,
    flow: str = "",
    public_port: int | None = None,
) -> str:
    stream = inbound.stream_settings
    security = stream.get("security", "none")
    network = stream.get("network", "tcp")
    params: dict[str, str] = {
        "type": network,
        "encryption": "none",
    }
    if flow:
        params["flow"] = flow
    if security == "reality":
        reality = stream.get("realitySettings") or {}
        params["security"] = "reality"
        params["pbk"] = reality.get("publicKey", "")
        params["fp"] = reality.get("fingerprint", "chrome")
        server_names = reality.get("serverNames") or []
        if server_names:
            params["sni"] = server_names[0]
        short_ids = reality.get("shortIds") or []
        if short_ids:
            params["sid"] = short_ids[0]
        params["spx"] = reality.get("spiderX", "/")
    elif security == "tls":
        params["security"] = "tls"
    port = public_port or inbound.port
    query = urlencode(params, quote_via=quote, safe="/:")
    return f"vless://{client_id}@{host}:{port}?{query}#{email}"


def build_sub_url(base_url: str, sub_id: str) -> str:
    base = base_url.rstrip("/")
    return f"{base}/sub/{sub_id}"
