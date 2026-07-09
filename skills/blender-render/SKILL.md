---
name: blender-render
description: Render 3D scenes with Blender (>=5) following a house style — warm soft temperature-based lighting, an enclosing softly-lit sphere environment, wide-angle large-aperture cameras with depth of field and motion blur, and multiple animated cameras. Renders on the host GPU or in a reproducible Docker/CI image, outputs PNG frames encoded to MP4 with ffmpeg, and iterates with visual inspection of the artifacts. Use for any Blender rendering, 3D scene, animation, or product/hero shot.
---

# blender-render

Render Blender scenes to a consistent, cinematic house style. Assets live in
`assets/`; render with `blender -b -P assets/render.py -- <flags>`.

## House style (all on by default)
- **Renderer: Cycles** by default (path-traced, physically-based) with denoising
  on. Only switch to EEVEE when the user asks or a fast preview is explicitly
  needed — say so when you do.
- **Enclosing environment:** the scene sits inside a soft, warm, inside-out
  emissive **sphere** (plus an outer shell) so lighting is contained and even.
- **Warm soft lighting:** three-point setup of large area lights using the
  per-light **color temperature** control (native in Blender 4.2+/5.x; ~3000–3500 K
  key/fill). Falls back to Kelvin→RGB on older builds. See `assets/lighting.py`.
- **Wide-angle, large aperture:** 18 mm lens, f/1.4, **depth of field on**
  (focused on the hero object).
- **Motion blur on.**
- **Multiple animated cameras:** orbit, dolly-in, and crane, cut together across
  the timeline via camera markers for nice motion.

## Rendering

**Host GPU (fast, interactive):**
```sh
./assets/run_host.sh                        # animation → PNGs + MP4
./assets/run_host.sh --mode still           # single frame
BLENDER=/path/to/blender ./assets/run_host.sh --samples 256 --res 1920x1080
```
Requires a local Blender ≥5 and ffmpeg. Uses the host GPU (`--device GPU`,
auto-selects OPTIX/CUDA/HIP/METAL).

**Docker / CI (reproducible, CPU):** `assets/Dockerfile` builds a Blender ≥5 +
ffmpeg image. The `blender-renders` workflow renders a still and a short
animation on every change and uploads them as artifacts; it publishes the image
to `ghcr.io/<owner>/<repo>/blender`.

## Animations → MP4
`render.py` writes `frame_####.png`; `assets/encode.sh` turns them into an MP4
(`libx264`, `yuv420p`, crf 18). `run_host.sh` and CI do this automatically.

## ALWAYS: visual-inspection loop
After every render, **look at the artifacts** and iterate — do not stop at
"the render succeeded". See `references/inspection.md`. In short:
1. Open the still PNG / MP4 (or the first, middle, last frames).
2. Check exposure, framing, focus (DOF on the hero), and motion.
3. **If a label exists, verify it is readable and well placed** — in frame, not
   clipped, not overlapping the subject, legible against the background.
4. Fix (light power/temperature, aperture, focus object, label position) and
   re-render. Repeat until it looks right.

## Common flags (after `--`)
`--mode still|animation` · `--out PATH` · `--samples N` · `--res WxH` ·
`--start/--end` · `--fps N` · `--device GPU|CPU` · `--label TEXT`

See `references/lighting.md` for the lighting rationale and knobs.
