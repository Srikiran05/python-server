#!/usr/bin/env python3
"""
Multi-threaded Proxy Server
Usage: python proxy_server.py [HOST] [PORT]
Default: HOST=0.0.0.0, PORT=8888
"""

import socket
import threading
import struct
import requests
import sys

HOST = "0.0.0.0"
PORT = 8888
BACKLOG = 50
RECV_BUFFER = 4096
REQUEST_TIMEOUT = 15

def fetch_url(url: str) -> (bool, bytes): # type: ignore
    """Fetch URL with a browser-like User-Agent."""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
        }
        resp = requests.get(url, timeout=REQUEST_TIMEOUT, allow_redirects=True, headers=headers)
        resp.raise_for_status()
        return True, resp.content
    except Exception as e:
        return False, f"Error: {e}".encode("utf-8")

def handle_client(conn: socket.socket, addr):
    try:
        print(f"[+] Connection from {addr}")

        # Read URL until newline
        data = b""
        while b"\n" not in data:
            chunk = conn.recv(RECV_BUFFER)
            if not chunk:
                return
            data += chunk
            if len(data) > 4096:
                return

        url = data.split(b"\n", 1)[0].decode("utf-8").strip()
        print(f"[>] Fetching: {url}")

        success, payload = fetch_url(url)

        # Protocol: 1 byte status + 8 byte length + payload
        status = b"\x00" if success else b"\x01"
        length = struct.pack("!Q", len(payload))
        conn.sendall(status + length + payload)

        print(f"[+] Sent {len(payload)} bytes to {addr}")
    except Exception as e:
        print(f"[!] Error handling {addr}: {e}")
    finally:
        conn.close()

def start_server(host=HOST, port=PORT):
    print(f"Starting proxy server on {host}:{port} ...")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((host, port))
    s.listen(BACKLOG)

    try:
        while True:
            conn, addr = s.accept()
            t = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
            t.start()
    except KeyboardInterrupt:
        print("\nShutting down.")
    finally:
        s.close()

if __name__ == "__main__":
    if len(sys.argv) >= 2:
        HOST = sys.argv[1]
    if len(sys.argv) >= 3:
        PORT = int(sys.argv[2])
    start_server(HOST, PORT)