# Visual-inspection loop

A render is not done when it finishes — it is done when it *looks right*. Always
open the artifacts and iterate.

## Loop
1. **Render** (start small: low samples/res for fast feedback).
2. **View the output.** For stills, open the PNG. For animations, view the MP4
   or at least the first / middle / last `frame_####.png`.
3. **Judge against intent:**
   - Exposure: not blown out, not muddy.
   - Framing/composition: subject well placed, headroom, no awkward crops.
   - Focus: DOF falls on the hero; foreground/background blur reads as intended.
   - Motion (animation): camera moves are smooth, no clipping through geometry,
     cuts land cleanly.
   - Lighting: warm and soft as intended; shadows not harsh; no black voids.
4. **Labels (if any):**
   - Fully inside the frame — not clipped at edges.
   - Not overlapping or obscuring the subject.
   - Legible: enough size and contrast against whatever is behind it.
   - Consistent position across all frames of an animation.
5. **Adjust and re-render.** Change one variable at a time (light power,
   temperature, aperture, focus object, label position/scale, camera keyframes).
6. Repeat until it meets the bar, then do a final high-sample/full-res render.

## Cheap ways to inspect
- Render a single representative still first; only commit to the full animation
  once the look is right.
- Sample frames: render just frames at the start, a middle cut, and the end.
- Use the CI artifacts (still PNG + short MP4) as the first-pass proof, then
  refine on the host GPU.

## Common fixes
| Symptom | Fix |
|---------|-----|
| Too dark/bright | light `energy`, exposure, denoise |
| Harsh shadows | larger light `size`, raise dome emission |
| Wrong thing in focus | camera `dof.focus_object` |
| Not enough blur | lower `aperture_fstop`; raise `motion_blur_shutter` |
| Label clipped/overlapping | adjust `Label` location/scale in `add_label` |
| Jerky camera | check keyframe spacing / interpolation |
