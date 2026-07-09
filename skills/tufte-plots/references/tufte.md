# Tufte's principles, applied

From *The Visual Display of Quantitative Information* and *Visual Explanations*.

## Data-ink ratio
Data-ink ÷ total-ink → 1. Every drop of ink should carry information. Erase
non-data ink (backgrounds, boxes, heavy grids) and redundant data-ink.

## Chartjunk
Remove moiré patterns, gratuitous grids, 3-D effects, and decoration. They add
noise, not signal.

## Range frames
Confine axis spines to the range of the data (`set_bounds`). The frame then
doubles as a summary of the data's extent.

## Direct labeling
Place labels next to the thing they describe (line ends, points) instead of a
separate legend. The eye shouldn't round-trip to a key.

## Small multiples
For comparisons, repeat a small, identical design across a series. Keep scales
and framing constant so differences are the only variable. Still: **one PDF per
panel** — assemble in the document, not the plot.

## Practical defaults (encoded in tufte.mplstyle)
- **Computer Modern serif** (`cmr10`, bundled with matplotlib) so figures match a
  LaTeX paper with no LaTeX install; math in matching `cm` mathtext. For an exact
  match to a specific document, enable `text.usetex: True` (needs a LaTeX
  toolchain). `axes.unicode_minus: False` so the minus renders via mathtext.
- Modest sizes; PDF (`fonttype 42` for editable text).
- No top/right spines, no grid, thin axes lines.
- Muted color cycle; near-black primary series.
- Small, outward tick marks.

## What to avoid
- Subplot grids in one file (breaks single-panel rule).
- Raster output (PNG/JPG) for line art — use PDF.
- Legends when 2–4 series can be labeled directly.
- Dual y-axes (usually misleading).
