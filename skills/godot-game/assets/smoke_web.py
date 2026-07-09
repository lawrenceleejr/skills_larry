#!/usr/bin/env python3
"""Smoke-test a Godot HTML5 export the way GitHub Pages will serve it.

Serves the export dir over plain HTTP (no COOP/COEP headers, like Pages), loads
index.html in headless Chromium, and checks the engine boots without fatal
errors. Exit 0 => safe to deploy to Pages; non-zero => do not deploy.

Usage: python smoke_web.py <web_dir> [--timeout 45]
"""
from __future__ import annotations

import argparse
import functools
import http.server
import socketserver
import sys
import threading
from pathlib import Path

from playwright.sync_api import sync_playwright


def serve(directory: Path):
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(directory))
    httpd = socketserver.TCPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd, httpd.server_address[1]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("web_dir")
    ap.add_argument("--timeout", type=int, default=45)
    args = ap.parse_args()

    web_dir = Path(args.web_dir)
    if not (web_dir / "index.html").exists():
        print(f"[smoke] no index.html in {web_dir}", file=sys.stderr)
        return 1

    httpd, port = serve(web_dir)
    url = f"http://127.0.0.1:{port}/index.html"
    print(f"[smoke] serving {web_dir} at {url}")

    errors: list[str] = []
    with sync_playwright() as p:
        browser = p.chromium.launch(args=["--use-gl=swiftshader", "--enable-webgl"])
        page = browser.new_page()
        page.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
        page.on("pageerror", lambda e: errors.append(str(e)))
        page.goto(url, timeout=args.timeout * 1000)

        # Wait for Godot's canvas to exist and gain a real drawing surface.
        try:
            page.wait_for_selector("#canvas", timeout=args.timeout * 1000)
            page.wait_for_function(
                "() => { const c = document.getElementById('canvas');"
                " return c && c.width > 0 && c.height > 0; }",
                timeout=args.timeout * 1000,
            )
        except Exception as e:  # noqa: BLE001
            print(f"[smoke] engine did not initialize: {e}", file=sys.stderr)
            browser.close(); httpd.shutdown()
            return 1
        browser.close()

    httpd.shutdown()
    fatal = [e for e in errors if "SharedArrayBuffer" in e or "abort" in e.lower()
             or "uncaught" in e.lower()]
    if fatal:
        print("[smoke] fatal errors:\n  " + "\n  ".join(fatal), file=sys.stderr)
        return 1
    print("[smoke] OK: Godot web build initialized in browser")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
