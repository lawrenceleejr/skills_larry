"""Subtle blurred drop shadows for matplotlib foreground artists.

A faint, offset, Gaussian-blurred shadow under a foreground element gently
suggests Z-order without adding chartjunk. Keep it *subtle* — low alpha, small
offset, modest blur.

Two mechanisms, chosen automatically:
- **Blurred** (preferred): a real Gaussian blur via the Agg renderer's filter
  hook. In vector output (PDF) matplotlib rasterizes just the shadowed artist
  (mixed-mode), so the rest of the figure stays vector.
- **Fallback**: if the renderer has no filter hook, a soft shadow faked by
  stacking a few low-alpha offset copies (fully vector).

Usage:
    from shadow import with_drop_shadow, add_drop_shadow
    ax.plot(x, y, path_effects=with_drop_shadow())          # any artist
    line, = ax.plot(x, y); add_drop_shadow(line)            # after the fact
"""
from __future__ import annotations

import numpy as np
from matplotlib.patheffects import AbstractPathEffect, Normal
from matplotlib.transforms import Affine2D


# --- numpy-only separable Gaussian (no scipy dependency) ------------------- #
def _smooth1d(x, window_len):
    s = np.r_[2 * x[0] - x[window_len:1:-1], x, 2 * x[-1] - x[-1:-window_len:-1]]
    w = np.hanning(window_len)
    y = np.convolve(w / w.sum(), s, mode="same")
    return y[window_len - 1:-window_len + 1]


def _smooth2d(a, sigma):
    window_len = max(int(sigma), 1) * 2 + 1
    a = np.apply_along_axis(_smooth1d, 0, a, window_len)
    a = np.apply_along_axis(_smooth1d, 1, a, window_len)
    return a


class _GaussianAlphaFilter:
    """Agg filter: blur the artist's alpha into a soft, single-color shadow."""

    def __init__(self, sigma, alpha, color):
        self.sigma = sigma
        self.alpha = alpha
        self.color = color

    def get_pad(self, dpi):
        return int(self.sigma * 3 / 72 * dpi)

    def __call__(self, im, dpi):
        pad = self.get_pad(dpi)
        ny, nx = im.shape[0], im.shape[1]
        padded = np.zeros((ny + 2 * pad, nx + 2 * pad, 4), dtype=float)
        padded[pad:pad + ny, pad:pad + nx, :] = im
        a = _smooth2d(padded[:, :, 3] * self.alpha, self.sigma / 72 * dpi)
        out = np.zeros_like(padded)
        out[:, :, 0], out[:, :, 1], out[:, :, 2] = self.color
        out[:, :, 3] = a
        return out, -pad, -pad


class DropShadow(AbstractPathEffect):
    """A subtle blurred drop shadow path effect.

    offset: shadow displacement in points (x right, y up).
    sigma:  blur radius in points. alpha: peak shadow opacity. color: RGB 0-1.
    """

    def __init__(self, offset=(1.5, -1.5), sigma=3.0, alpha=0.35, color=(0, 0, 0)):
        super().__init__(offset)
        self._filter = _GaussianAlphaFilter(sigma, alpha, color)
        self._color = color
        self._alpha = alpha

    def draw_path(self, renderer, gc, tpath, affine, rgbFace=None):
        ox, oy = self._offset
        shifted = affine + Affine2D().translate(
            renderer.points_to_pixels(ox), renderer.points_to_pixels(oy)
        )
        gc0 = renderer.new_gc()
        gc0.copy_properties(gc)
        if hasattr(renderer, "start_filter"):
            # True Gaussian blur (rasterized for this artist only). Draw with the
            # artist's own face/stroke so the shadow matches its shape (a line
            # stays a line, a filled patch stays filled); the filter recolors it.
            renderer.start_filter()
            renderer.draw_path(gc0, tpath, shifted, rgbFace)
            renderer.stop_filter(self._filter)
        else:
            # Vector fallback: stack a few faint offset copies for a soft edge.
            gc0.set_foreground(self._color)
            face = (*self._color, 1.0) if rgbFace is not None else None
            layers = 4
            for i in range(layers):
                gc0.set_alpha(self._alpha / layers)
                spread = Affine2D().scale(1 + 0.004 * i)
                renderer.draw_path(gc0, tpath, shifted + spread, face)
        gc0.restore()


def with_drop_shadow(**kwargs):
    """Path-effect list: shadow underneath, then the artist drawn normally."""
    return [DropShadow(**kwargs), Normal()]


def add_drop_shadow(artist, **kwargs):
    """Attach a subtle blurred drop shadow to an existing artist."""
    effects = [DropShadow(**kwargs), Normal()]
    try:
        for a in artist:                    # handle lists (e.g. bar containers)
            a.set_path_effects(effects)
    except TypeError:
        artist.set_path_effects(effects)
    return artist
