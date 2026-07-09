#!/usr/bin/env python3
"""Validate that every skill has well-formed YAML frontmatter.

Each skills/<name>/SKILL.md must start with a --- fenced block containing
`name` and `description`, and `name` must match the directory.
"""
from __future__ import annotations

import sys
from pathlib import Path

SKILLS_DIR = Path(__file__).resolve().parents[1] / "skills"


def parse_frontmatter(text: str) -> dict[str, str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError("missing opening --- frontmatter fence")
    fm: dict[str, str] = {}
    for line in lines[1:]:
        if line.strip() == "---":
            return fm
        if ":" in line:
            key, _, val = line.partition(":")
            fm[key.strip()] = val.strip()
    raise ValueError("missing closing --- frontmatter fence")


def main() -> int:
    errors: list[str] = []
    skills = sorted(SKILLS_DIR.glob("*/SKILL.md"))
    if not skills:
        print("no skills found", file=sys.stderr)
        return 1
    for skill in skills:
        rel = skill.relative_to(SKILLS_DIR.parent)
        try:
            fm = parse_frontmatter(skill.read_text())
        except ValueError as e:
            errors.append(f"{rel}: {e}")
            continue
        for field in ("name", "description"):
            if not fm.get(field):
                errors.append(f"{rel}: frontmatter missing '{field}'")
        if fm.get("name") and fm["name"] != skill.parent.name:
            errors.append(
                f"{rel}: name '{fm['name']}' != directory '{skill.parent.name}'"
            )
        if len(fm.get("description", "")) < 20:
            errors.append(f"{rel}: description too short to be useful")

    if errors:
        print("Skill validation failed:", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1
    print(f"OK: {len(skills)} skills valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
