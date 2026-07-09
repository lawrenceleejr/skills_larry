---
name: typography
description: Set type using freely-available Google Fonts, applying font-pairing and visual-hierarchy principles. Use whenever choosing fonts or typesetting anything with text — websites, apps, plots/figures, slides, game UI, PDFs, or artifacts.
---

# typography

Whenever text appears, set it deliberately. Use **Google Fonts** (all free —
OFL/Apache/UFL, safe to bundle), pair fonts on principle, and enforce hierarchy.

## Font choice
- Pick from Google Fonts so licensing is never a question and the family is
  fetchable in CI/Docker.
- **Self-host for reproducibility** with `assets/get_fonts.py` — it downloads the
  woff2 files and writes a `fonts.css`, so builds don't depend on a runtime CDN:
  ```sh
  ./get_fonts.py --out static/fonts "Fraunces:wght@400;600;900" "Inter:wght@400;500;700"
  ```
  Do the download inside your build's Docker image (see `docker-run`).
- For matplotlib/PDFs, register the .ttf/.otf and set `font.family` (pairs with
  the `tufte-plots` style).

## Pairing principles
1. **Contrast with harmony:** pair fonts that differ clearly in role but share a
   mood — classic combo is a **serif display + sans body** (or vice versa).
2. **Limit to two families** (plus a mono for code). More reads as noise.
3. **Superfamilies are a safe default:** one family with matched sans/serif
   (e.g. IBM Plex, Source, Noto) pairs by construction.
4. **Match x-height and proportions** so sizes feel consistent across families.
5. **Give each font one job:** headings vs. body vs. code — don't mix roles.

Curated, safe pairings are in `references/pairings.md`.

## Hierarchy principles
- **One type scale.** Use a modular scale (e.g. 1.25×): 12·15·19·23·29·37…
  rather than arbitrary sizes.
- **Establish rank with size, weight, and space** — not color alone.
- **Body text 16px+**, line-height ~1.5, measure **45–75 characters** per line.
- **Headings:** heavier weight, tighter line-height, generous space *above* >
  below (group with what they title).
- **Restraint:** few weights (e.g. 400/600/900), sentence case, avoid ALL-CAPS
  except small labels (add letter-spacing there).
- **Align to a baseline/spacing rhythm**; consistent vertical spacing beats
  ad-hoc margins.

## Checklist
- [ ] Fonts are from Google Fonts and self-hosted for the build
- [ ] Two families max (+ optional mono), distinct roles
- [ ] A single modular type scale drives all sizes
- [ ] Body ≥16px, line-height ~1.5, measure 45–75ch
- [ ] Hierarchy reads without relying on color
