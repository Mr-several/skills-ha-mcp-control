#!/usr/bin/env python3
"""Capture a current frame from a Home Assistant camera entity."""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import pathlib
import shutil
import socket
import ssl
import struct
import subprocess
import sys
import tempfile
import urllib.parse
from dataclasses import dataclass
from typing import Any


class ConfigError(RuntimeError):
    pass


class HaApiError(RuntimeError):
    pass


@dataclass
class HaCredentials:
    base_url: str
    token: str
    source: str


def _load_json(path: pathlib.Path) -> dict[str, Any] | None:
    if not path.is_file():
        return None
    return json.loads(path.read_text())


def _normalize_http_base(url: str) -> str:
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme in {"http", "https"}:
        return f"{parsed.scheme}://{parsed.netloc}"
    if parsed.scheme in {"ws", "wss"}:
        http_scheme = "https" if parsed.scheme == "wss" else "http"
        return f"{http_scheme}://{parsed.netloc}"
    raise ConfigError(f"Unsupported Home Assistant URL scheme: {url}")


def _resolve_credentials() -> HaCredentials:
    env_url = os.environ.get("HOMEASSISTANT_URL")
    env_token = os.environ.get("HOMEASSISTANT_TOKEN")
    if env_url and env_token:
        return HaCredentials(_normalize_http_base(env_url), env_token, "env")

    cwd = pathlib.Path.cwd()
    mcporter_candidates = [
        cwd / "openclaw" / "config" / "mcporter.json",
        cwd / "config" / "mcporter.json",
        pathlib.Path.home() / ".mcporter" / "mcporter.json",
    ]
    for candidate in mcporter_candidates:
        data = _load_json(candidate)
        if not data:
            continue
        servers = data.get("mcpServers") or {}
        for name, cfg in servers.items():
            env = cfg.get("env") or {}
            url = env.get("HOMEASSISTANT_URL")
            token = env.get("HOMEASSISTANT_TOKEN")
            if url and token:
                return HaCredentials(_normalize_http_base(url), token, f"mcporter:{candidate}:{name}")

    openclaw_config_path = os.environ.get("OPENCLAW_CONFIG_PATH")
    openclaw_candidates = [
        pathlib.Path(openclaw_config_path).expanduser() if openclaw_config_path else None,
        pathlib.Path.home() / ".openclaw" / "openclaw.json",
        pathlib.Path.home() / ".openclaw-dev" / "openclaw.json",
    ]
    for candidate in openclaw_candidates:
        if candidate is None:
            continue
        data = _load_json(candidate)
        if not data:
            continue
        cfg = ((data.get("plugins") or {}).get("entries") or {}).get("ha-bridge") or {}
        plugin_cfg = cfg.get("config") or {}
        ws_url = plugin_cfg.get("haWsUrl")
        token = plugin_cfg.get("haToken")
        if ws_url and token:
            return HaCredentials(_normalize_http_base(ws_url), token, f"ha-bridge:{candidate}")

    raise ConfigError("Home Assistant credentials not found")


def _ws_connect(ws_url: str) -> socket.socket:
    parsed = urllib.parse.urlparse(ws_url)
    if parsed.scheme not in {"ws", "wss"}:
        raise ConfigError(f"Unsupported websocket URL: {ws_url}")
    host = parsed.hostname
    if not host:
        raise ConfigError(f"Invalid websocket URL: {ws_url}")
    port = parsed.port or (443 if parsed.scheme == "wss" else 80)
    path = parsed.path or "/"
    if parsed.query:
        path += f"?{parsed.query}"
    raw_sock = socket.create_connection((host, port), timeout=15)
    sock: socket.socket
    if parsed.scheme == "wss":
        ctx = ssl.create_default_context()
        sock = ctx.wrap_socket(raw_sock, server_hostname=host)
    else:
        sock = raw_sock
    key = base64.b64encode(os.urandom(16)).decode("ascii")
    request = (
        f"GET {path} HTTP/1.1\r\n"
        f"Host: {host}:{port}\r\n"
        "Upgrade: websocket\r\n"
        "Connection: Upgrade\r\n"
        f"Sec-WebSocket-Key: {key}\r\n"
        "Sec-WebSocket-Version: 13\r\n"
        "\r\n"
    )
    sock.sendall(request.encode("ascii"))
    response = b""
    while b"\r\n\r\n" not in response:
        chunk = sock.recv(4096)
        if not chunk:
            raise HaApiError("WebSocket handshake failed")
        response += chunk
    header = response.split(b"\r\n\r\n", 1)[0].decode("iso-8859-1")
    if " 101 " not in header:
        raise HaApiError(f"WebSocket handshake failed: {header}")
    expected = base64.b64encode(
        hashlib.sha1((key + "258EAFA5-E914-47DA-95CA-C5AB0DC85B11").encode("ascii")).digest()
    ).decode("ascii")
    if f"Sec-WebSocket-Accept: {expected}" not in header:
        raise HaApiError("Invalid WebSocket accept header")
    return sock


def _ws_send_text(sock: socket.socket, text: str) -> None:
    payload = text.encode("utf-8")
    header = bytearray([0x81])
    length = len(payload)
    mask_bit = 0x80
    if length < 126:
        header.append(mask_bit | length)
    elif length < (1 << 16):
        header.append(mask_bit | 126)
        header.extend(struct.pack("!H", length))
    else:
        header.append(mask_bit | 127)
        header.extend(struct.pack("!Q", length))
    mask = os.urandom(4)
    header.extend(mask)
    masked = bytes(b ^ mask[i % 4] for i, b in enumerate(payload))
    sock.sendall(bytes(header) + masked)


def _recv_exact(sock: socket.socket, size: int) -> bytes:
    data = b""
    while len(data) < size:
        chunk = sock.recv(size - len(data))
        if not chunk:
            raise HaApiError("Unexpected websocket EOF")
        data += chunk
    return data


def _ws_recv_text(sock: socket.socket) -> str:
    while True:
        first, second = _recv_exact(sock, 2)
        opcode = first & 0x0F
        masked = bool(second & 0x80)
        length = second & 0x7F
        if length == 126:
            length = struct.unpack("!H", _recv_exact(sock, 2))[0]
        elif length == 127:
            length = struct.unpack("!Q", _recv_exact(sock, 8))[0]
        mask = _recv_exact(sock, 4) if masked else b""
        payload = _recv_exact(sock, length)
        if masked:
            payload = bytes(b ^ mask[i % 4] for i, b in enumerate(payload))
        if opcode == 0x9:
            pong = bytearray([0x8A, len(payload)])
            sock.sendall(bytes(pong) + payload)
            continue
        if opcode == 0x8:
            raise HaApiError("WebSocket closed by Home Assistant")
        if opcode != 0x1:
            continue
        return payload.decode("utf-8")


def _get_hls_url(credentials: HaCredentials, entity_id: str) -> str:
    ws_url = credentials.base_url.replace("http://", "ws://", 1).replace("https://", "wss://", 1) + "/api/websocket"
    sock = _ws_connect(ws_url)
    try:
        hello = json.loads(_ws_recv_text(sock))
        if hello.get("type") != "auth_required":
            raise HaApiError(f"Unexpected websocket hello: {hello}")
        _ws_send_text(sock, json.dumps({"type": "auth", "access_token": credentials.token}))
        auth = json.loads(_ws_recv_text(sock))
        if auth.get("type") != "auth_ok":
            raise HaApiError(f"Home Assistant websocket auth failed: {auth}")
        _ws_send_text(sock, json.dumps({"id": 1, "type": "camera/stream", "entity_id": entity_id}))
        result = json.loads(_ws_recv_text(sock))
        if not result.get("success"):
            raise HaApiError(f"camera/stream failed: {result}")
        path = ((result.get("result") or {}).get("url"))
        if not path:
            raise HaApiError(f"camera/stream returned no URL: {result}")
        return credentials.base_url + path
    finally:
        try:
            sock.close()
        except OSError:
            pass


def _require_ffmpeg() -> str:
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        raise RuntimeError("ffmpeg not found in PATH")
    return ffmpeg


def _capture_frame(ffmpeg: str, token: str, hls_url: str, output: pathlib.Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        ffmpeg,
        "-y",
        "-loglevel",
        "error",
        "-headers",
        f"Authorization: Bearer {token}\r\n",
        "-i",
        hls_url,
        "-frames:v",
        "1",
        str(output),
    ]
    subprocess.run(cmd, check=True)


def _default_output(entity_id: str) -> pathlib.Path:
    safe = entity_id.replace(".", "_")
    return pathlib.Path(tempfile.gettempdir()) / f"{safe}_frame.jpg"


def main() -> int:
    parser = argparse.ArgumentParser(description="Capture a current frame from a Home Assistant camera entity")
    parser.add_argument("--entity-id", required=True, help="Home Assistant camera entity_id")
    parser.add_argument("--output", help="Output image path")
    args = parser.parse_args()

    try:
        credentials = _resolve_credentials()
        ffmpeg = _require_ffmpeg()
        hls_url = _get_hls_url(credentials, args.entity_id)
        output = pathlib.Path(args.output).expanduser() if args.output else _default_output(args.entity_id)
        _capture_frame(ffmpeg, credentials.token, hls_url, output)
        result = {
            "entity_id": args.entity_id,
            "output": str(output),
            "base_url": credentials.base_url,
            "credential_source": credentials.source,
            "hls_url": hls_url,
        }
        print(json.dumps(result, ensure_ascii=False))
        return 0
    except (ConfigError, HaApiError, subprocess.CalledProcessError, RuntimeError) as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
