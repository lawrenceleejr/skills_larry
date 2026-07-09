"""Self-contained example analysis: uproot I/O + hist + Tufte single-panel PDF.

Demonstrates the repo conventions:
- uproot for ROOT I/O (no PyROOT),
- hist for histogramming,
- a single-panel PDF plot following the tufte-plots style.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

# Make the tufte helpers/style importable regardless of CWD.
REPO = Path(__file__).resolve().parents[2]
TUFTE_ASSETS = REPO / "skills" / "tufte-plots" / "assets"
sys.path.insert(0, str(TUFTE_ASSETS))


def make_dataset(n: int = 20_000, seed: int = 1234) -> np.ndarray:
    """Synthetic transverse-momentum-like sample (falling spectrum)."""
    rng = np.random.default_rng(seed)
    # Exponential falling spectrum, GeV-ish scale.
    return rng.exponential(scale=40.0, size=n).astype(np.float32)


def roundtrip_root(pt: np.ndarray, path: str | Path) -> np.ndarray:
    """Write pt to a ROOT file and read it back with uproot (no PyROOT)."""
    import uproot

    path = Path(path)
    with uproot.recreate(path) as f:
        f["Events"] = {"pt": pt}
    with uproot.open(path) as f:
        return f["Events"]["pt"].array(library="np")


def histogram(pt: np.ndarray):
    """Fill a 1D histogram of pt with scikit-hep `hist`."""
    import hist

    h = hist.Hist(hist.axis.Regular(50, 0, 200, name="pt", label=r"$p_T$ [GeV]"))
    h.fill(pt=pt)
    return h


def plot_pdf(h, out_path: str | Path) -> Path:
    """Render the histogram as a single-panel Tufte-style PDF."""
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    from tufte_helpers import save_pdf, spines_to_data_range  # type: ignore

    plt.style.use(str(TUFTE_ASSETS / "tufte.mplstyle"))

    centers = h.axes[0].centers
    values = h.values()

    fig, ax = plt.subplots(figsize=(4, 3))  # single panel
    ax.step(centers, values, where="mid")
    ax.set_xlabel(r"$p_T$ [GeV]")
    ax.set_ylabel("Events / 4 GeV")
    spines_to_data_range(ax)
    return save_pdf(fig, out_path)


def run(out_dir: str | Path = "output") -> Path:
    """End-to-end: generate → ROOT roundtrip → histogram → PDF."""
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    pt = make_dataset()
    pt = roundtrip_root(pt, out_dir / "events.root")
    h = histogram(pt)
    return plot_pdf(h, out_dir / "pt_spectrum.pdf")
