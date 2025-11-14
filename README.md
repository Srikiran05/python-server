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
