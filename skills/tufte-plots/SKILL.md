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
