# PyROOT → uproot cheatsheet

| Task | PyROOT | uproot / scikit-hep |
|------|--------|---------------------|
| Open file | `ROOT.TFile.Open("f.root")` | `uproot.open("f.root")` |
| Get tree | `f.Get("Events")` | `f["Events"]` |
| List branches | `tree.GetListOfBranches()` | `tree.keys()` |
| Read branches | event loop `tree.GetEntry(i)` | `tree.arrays(["pt"], library="ak")` |
| Many files | `TChain` | `uproot.iterate("*.root:Events", ...)` |
| Histogram | `ROOT.TH1F(...)`, `Fill` | `hist.Hist(hist.axis.Regular(...))`, `.fill` |
| Write tree | `TTree` + `Branch` + `Fill` | `uproot.recreate(...)["t"] = {...}` |
| Cut / selection | `TTree.Draw("pt", "eta<2.4")` | `data[data.eta < 2.4]` (awkward) |

## Selections with awkward
```python
import awkward as ak
sel = (data.pt > 20) & (abs(data.eta) < 2.4)
data[sel]                      # event mask
data.pt[data.pt > 20]         # jagged mask, per-object
ak.num(data.pt)               # multiplicity per event
```

## When PyROOT is still needed
- RooFit-based fits without a scikit-hep equivalent (`zfit`/`iminuit` often
  suffice — prefer them).
- Reading exotic/legacy streamer types uproot doesn't support yet.
State the reason in code comments and keep it isolated from the main pipeline.
