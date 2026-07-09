"""Entry point for the example workload."""
from __future__ import annotations

import sys

from analysis import run


def main(argv: list[str]) -> int:
    out = run(argv[0] if argv else "output")
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
