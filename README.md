# Multi-threaded Proxy Server & Client

A **lightweight, multi-threaded HTTP proxy** built in Python that:
- Accepts **any URL** from the client
- Fetches the content via the server
- Returns it to the client
- Saves the output as an **HTML file** with an **appropriate name**

---

## Features

- **Multi-threaded server** → Handles multiple clients concurrently
- **Simple protocol** → `URL\n` → `status(1) + length(8) + payload`
- **Smart filename generation** → `host_path.html` (e.g., `wikipedia.org_index.html`)
- **Error handling** → Saves server errors to file for debugging
- **User-Agent support** → Bypasses 403 on Wikipedia, Reddit, etc.
- **No external dependencies** (except `requests`)

---
## Requirements
- Python 3.6+

- `requests` library

```bash
pip install requests
```
## How to run
### Step - 1 ( Start the Proxy Server )
Open a terminal and run 
```bash
python proxy_server.py
```
You'll see
```bash
Starting proxy server on 0.0.0.0:8888 ...
```
### Step - 2 ( Use the client in another terminal )
```bash
python proxy_client.py SERVER_HOST SERVER_PORT "URL"
```
Expected output:
```bash
Connecting to localhost:8080 ...
```
Status=OK, Size=85421 bytes
[+] Saved HTML to 'example.com_index.html' (85421 bytes)

Open the .html file in your browser → full page!
