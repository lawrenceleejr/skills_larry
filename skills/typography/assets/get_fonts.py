#!/usr/bin/env python3
"""Download Google Fonts for self-hosting (reproducible, no runtime CDN).

Fetches the woff2 files behind the Google Fonts CSS2 API and writes a local
`fonts.css` with @font-face rules pointing at the downloaded files. Self-hosting
keeps builds reproducible and avoids a third-party request at runtime.

Usage:
  ./get_fonts.py --out static/fonts \\
      "Fraunces:wght@400;600;900" "Inter:wght@400;500;700"

All Google Fonts are free (OFL/Apache/UFL) — safe to bundle and redistribute.
"""
from __future__ import annotations

import argparse
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path

# A modern UA so the API returns woff2 (its smallest, widely-supported format).
UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
      "Chrome/120.0 Safari/537.36")

FACE_RE = re.compile(r"@font-face\s*\{([^}]*)\}", re.S)
PROP_RE = lambda k: re.compile(rf"{k}:\s*([^;]+);")  # noqa: E731
URL_RE = re.compile(r"url\(([^)]+)\)")


def fetch(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:  # noqa: S310
        return r.read().decode("utf-8")


def slug(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="fonts", help="output directory")
    ap.add_argument("families", nargs="+",
                    help='e.g. "Inter:wght@400;700" (as in the Google Fonts URL)')
    args = ap.parse_args()

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    query = "&".join(f"family={urllib.parse.quote(f, safe=':;@,')}" for f in args.families)
    css = fetch(f"https://fonts.googleapis.com/css2?{query}&display=swap")

    rules: list[str] = []
    n = 0
    for block in FACE_RE.findall(css):
        fam = PROP_RE("font-family").search(block)
        weight = PROP_RE("font-weight").search(block)
        style = PROP_RE("font-style").search(block)
        url = URL_RE.search(block)
        if not (fam and url):
            continue
        family = fam.group(1).strip().strip('"')
        w = weight.group(1).strip() if weight else "400"
        st = style.group(1).strip() if style else "normal"
        remote = url.group(1).strip().strip('"')
        n += 1
        fname = f"{slug(family)}-{slug(w)}-{st}-{n}.woff2"
        (out / fname).write_bytes(urllib.request.urlopen(  # noqa: S310
            urllib.request.Request(remote, headers={"User-Agent": UA})).read())
        unicode_range = PROP_RE("unicode-range").search(block)
        ur = f"\n  unicode-range: {unicode_range.group(1).strip()};" if unicode_range else ""
        rules.append(
            f"@font-face {{\n  font-family: '{family}';\n  font-style: {st};\n"
            f"  font-weight: {w};\n  font-display: swap;\n"
            f"  src: url('{fname}') format('woff2');{ur}\n}}"
        )

    if not rules:
        print("[get_fonts] no @font-face rules parsed — check family specs", file=sys.stderr)
        return 1
    (out / "fonts.css").write_text("\n".join(rules) + "\n")
    print(f"[get_fonts] wrote {n} woff2 file(s) + fonts.css to {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
