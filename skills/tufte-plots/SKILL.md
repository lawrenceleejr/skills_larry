---
name: tufte-plots
description: Create single-panel, PDF-output plots that follow Edward Tufte's principles (maximize data-ink, remove chartjunk). Use whenever generating any chart, plot, or figure for a paper, report, or analysis with matplotlib or similar.
---

# tufte-plots

Every plot follows Tufte's principles and these hard rules:

- **One panel per file.** No subplot grids. If you need N panels, write N PDFs.
- **PDF output.** Vector, publication-ready. `fig.savefig("name.pdf")`.
- **Maximize the data-ink ratio.** Erase everything that isn't data.

## Fast path

Use the provided matplotlib style, then plot normally:

The style defaults to a **Computer Modern serif** (`cmr10`, bundled with
matplotlib) so figures drop into a LaTeX paper looking native — no LaTeX install
required. For an exact match to a specific document, uncomment `text.usetex` in
the style (needs a LaTeX toolchain).

```python
import matplotlib.pyplot as plt
plt.style.use("skills/tufte-plots/assets/tufte.mplstyle")

fig, ax = plt.subplots(figsize=(4, 3))   # single panel
ax.plot(x, y)
ax.set_xlabel("x")
ax.set_ylabel("y")
fig.savefig("figure.pdf", bbox_inches="tight")
```

`assets/tufte_helpers.py` provides `spines_to_data_range(ax)` (Tufte range
frames) and `save_pdf(fig, path)` (enforces PDF + tight bbox).

## Subtle drop shadows (optional Z-order cue)
To *gently* suggest that foreground elements sit above the plane, add a faint,
blurred drop shadow via `assets/shadow.py`. Keep it subtle — it's a hint, not
decoration (and it is the one deliberate exception to strict data-ink).

```python
from shadow import with_drop_shadow, add_drop_shadow
ax.plot(x, y, path_effects=with_drop_shadow())      # at draw time
add_drop_shadow(ax.bar(cats, vals))                 # or after the fact
# tune: with_drop_shadow(offset=(2,-2), sigma=7, alpha=0.4)
```

Defaults are soft and understated (offset 2pt, blur σ=7pt, alpha 0.4); raise
`sigma` for an even more diffuse shadow.
The blur is a real Gaussian: in **PDF** output matplotlib rasterizes only the
shadowed artist (mixed-mode) while the rest of the figure stays vector. Use it
sparingly — one or two foreground layers, not everything.

## The rules (see references/tufte.md for rationale)

1. **No chartjunk:** no gridlines, no background fill, no boxes, no legends when
   direct labels work, no redundant ticks.
2. **Range frames:** spines span only the data range, not the whole axes.
3. **Direct labeling:** label lines at their end rather than in a legend.
4. **Minimal ticks:** few, meaningful tick marks; let data set the extent.
5. **Muted ink:** thin lines, restrained color, high contrast only for data.
6. **Small multiples**, when comparing — but still one PDF per panel.

## Checklist before saving
- [ ] Single panel, saved as `.pdf`
- [ ] Gridlines and top/right spines removed
- [ ] Axes labeled; units where relevant
- [ ] No legend if direct labels suffice
- [ ] Line/marker ink minimized
