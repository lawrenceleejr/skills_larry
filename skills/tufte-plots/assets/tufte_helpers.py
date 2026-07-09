"""Helpers for Tufte-style single-panel PDF plots."""
from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt


def spines_to_data_range(ax: plt.Axes) -> None:
    """Turn the left/bottom spines into range frames spanning only the data.

    Tufte's range frame: the axis line itself communicates the data extent.
    """
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    xticks = ax.get_xticks()
    yticks = ax.get_yticks()
    xdata = [t for t in xticks if ax.get_xlim()[0] <= t <= ax.get_xlim()[1]]
    ydata = [t for t in yticks if ax.get_ylim()[0] <= t <= ax.get_ylim()[1]]
    if xdata:
        ax.spines["bottom"].set_bounds(min(xdata), max(xdata))
    if ydata:
        ax.spines["left"].set_bounds(min(ydata), max(ydata))


def save_pdf(fig: plt.Figure, path: str | Path) -> Path:
    """Save as a single-panel PDF with a tight bounding box.

    Enforces the .pdf extension and errors if the figure has more than one panel.
    """
    path = Path(path).with_suffix(".pdf")
    n_axes = len(fig.axes)
    if n_axes > 1:
        raise ValueError(
            f"Tufte rule: one panel per file, but figure has {n_axes} axes. "
            "Write one PDF per panel."
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, format="pdf", bbox_inches="tight")
    return path
