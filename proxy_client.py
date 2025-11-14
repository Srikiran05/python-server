#!/usr/bin/env python3
"""
Proxy Client
Usage:
  python proxy_client.py SERVER_HOST SERVER_PORT "http://wikipedia.com" [-o output.html]
"""

import socket
import struct
import sys
import urllib.parse
import os

RECV_BUFFER = 8192

def sanitize_filename(s: str) -> str:
    keep = "-_.() abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    return "".join(c if c in keep else "_" for c in s).strip() or "output.html"

def generate_filename(url: str) -> str:
    parsed = urllib.parse.urlparse(url)
    host = parsed.netloc.replace(":", "_")
    path = parsed.path.rstrip("/") or "index"
    path = path.replace("/", "_")
    return sanitize_filename(f"{host}_{path}.html")

def recv_exact(sock: socket.socket, n: int) -> bytes:
    data = b""
    while len(data) < n:
        chunk = sock.recv(min(n - len(data), RECV_BUFFER))
        if not chunk:
            raise ConnectionError("Socket closed")
        data += chunk
    return data

def request_and_save(server_host, server_port, url, out_filename=None):
    if out_filename is None:
        out_filename = generate_filename(url)

    print(f"Connecting to {server_host}:{server_port} ...")
    with socket.create_connection((server_host, server_port), timeout=20) as s:
        s.sendall((url.strip() + "\n").encode("utf-8"))

        status = recv_exact(s, 1)[0]
        length = struct.unpack("!Q", recv_exact(s, 8))[0]
        print(f"Status={'OK' if status == 0 else 'ERROR'}, Size={length} bytes")

        received = 0
        with open(out_filename, "wb") as f:
            while received < length:
                chunk = s.recv(min(RECV_BUFFER, length - received))
                if not chunk:
                    raise ConnectionError("Incomplete data")
                f.write(chunk)
                received += len(chunk)

        if status == 0:
            print(f"[+] Saved HTML to '{out_filename}' ({length} bytes)")
        else:
            print(f"[!] Error saved to '{out_filename}'")
            with open(out_filename, "r", encoding="utf-8", errors="replace") as f:
                print(f.read(512))

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python proxy_client.py HOST PORT URL [-o output.html]")
        sys.exit(1)

    host = sys.argv[1]
    port = int(sys.argv[2])
    url = sys.argv[3]
    out = None
    if "-o" in sys.argv:
        idx = sys.argv.index("-o")
        if idx + 1 < len(sys.argv):
            out = sys.argv[idx + 1]

    request_and_save(host, port, url, out)