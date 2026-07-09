import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import analysis  # noqa: E402


def test_make_dataset_shape_and_positivity():
    pt = analysis.make_dataset(n=1000, seed=1)
    assert pt.shape == (1000,)
    assert (pt >= 0).all()


def test_roundtrip_root_preserves_data(tmp_path):
    pt = analysis.make_dataset(n=500, seed=2)
    back = analysis.roundtrip_root(pt, tmp_path / "e.root")
    np.testing.assert_allclose(back, pt, rtol=1e-6)


def test_histogram_conserves_counts():
    pt = analysis.make_dataset(n=5000, seed=3)
    h = analysis.histogram(pt)
    in_range = ((pt >= 0) & (pt < 200)).sum()
    assert h.values().sum() == in_range


def test_plot_writes_single_panel_pdf(tmp_path):
    pt = analysis.make_dataset(n=2000, seed=4)
    h = analysis.histogram(pt)
    out = analysis.plot_pdf(h, tmp_path / "fig")
    assert out.suffix == ".pdf"
    assert out.exists() and out.stat().st_size > 0
    # PDF magic number.
    assert out.read_bytes()[:4] == b"%PDF"
