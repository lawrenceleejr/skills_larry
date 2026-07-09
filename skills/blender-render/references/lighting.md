# Lighting rationale

## Warm & soft by default
- **Soft** comes from *large* emitters. Area lights with a big `size` (and the
  enclosing emissive sphere) produce broad, wrapping shadows. Small/point lights
  give hard, harsh shadows — avoid unless intentional.
- **Warm** comes from color temperature ~3000–3500 K (key/fill). Cooler light
  (~4500 K) on the rim adds separation without going cold.

## Color temperature (Blender 4.2+/5.x)
Recent Blender exposes a native Kelvin control on lights. `lighting.set_temperature`
uses it when available:
```python
light.use_temperature = True
light.temperature = 3200   # Kelvin; lower = warmer
```
On older builds it falls back to a blackbody Kelvin→RGB approximation.

Reference points: 2700 K tungsten (very warm) · 3200 K studio warm ·
4000 K neutral-warm · 5600 K daylight · 6500 K cool.

## Three-point setup (`three_point_warm`)
- **Key** — main light, strongest, ~45° off axis, warmest.
- **Fill** — large & soft, opposite the key, lower power, softens shadows.
- **Rim/back** — behind subject, slightly cooler, separates it from the
  background.

## Enclosing sphere environment
An inside-out emissive UV sphere wraps the scene in even, warm ambient light and
prevents black voids — like shooting inside a lightbox. Keep its emission low
(~1–1.5) so the three-point lights still shape the subject; raise it for flatter,
softer product shots.

## Knobs to tune during inspection
- Under/over-exposed → adjust light `energy` or samples/denoise.
- Too flat → raise key:fill ratio.
- Too cold/warm → shift `temperature`.
- Want more/less blur → camera `dof.aperture_fstop` (smaller = blurrier) and
  `render.motion_blur_shutter`.
