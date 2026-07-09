---
name: uproot-analysis
description: Read and analyze ROOT files with uproot + awkward array instead of PyROOT/HEP ROOT. Use for any high-energy-physics data I/O, TTree reading, or histogramming in Python where PyROOT would otherwise be reached for.
---

# uproot-analysis

Use `uproot` (+ `awkward`, `numpy`, and `hist`) for ROOT I/O. Reach for PyROOT
only when a feature genuinely has no `uproot` equivalent (e.g. certain
RooFit workflows) — and say so explicitly.

## Why
- Pure Python/NumPy: installs via pip, no ROOT build, works in slim Docker
  images and CI.
- Columnar and lazy: read only the branches you need.
- Interoperates with the scientific Python stack (awkward, pandas, hist).

## Reading a TTree

```python
import uproot

with uproot.open("file.root") as f:
    tree = f["Events"]
    # Read only needed branches; arrays are awkward/numpy.
    data = tree.arrays(["pt", "eta"], library="ak")

# Lazy / chunked over many files:
for chunk in uproot.iterate("data/*.root:Events", ["pt", "eta"], step_size="100 MB"):
    process(chunk)
```

## Histogramming

Use `hist` (scikit-hep), then plot with the `tufte-plots` skill (single-panel
PDF):

```python
import hist

h = hist.Hist(hist.axis.Regular(50, 0, 200, name="pt", label="$p_T$ [GeV]"))
h.fill(pt=data.pt)
# plot h.values() / h.axes[0].centers with matplotlib -> save PDF
```

## Writing ROOT files

```python
with uproot.recreate("out.root") as f:
    f["Events"] = {"pt": data.pt, "eta": data.eta}
```

See `references/cheatsheet.md` for common PyROOT → uproot translations.
