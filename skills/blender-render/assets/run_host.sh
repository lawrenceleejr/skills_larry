#!/usr/bin/env bash
# Render on the HOST using the host GPU (no Docker). Requires a local Blender >=5
# and (for animations) ffmpeg. For CI/reproducible CPU renders, use Docker instead.
#
#   ./run_host.sh                         # animation -> PNGs + MP4 via ffmpeg
#   ./run_host.sh --mode still            # single frame PNG
#   BLENDER=/path/to/blender ./run_host.sh --samples 256 --res 1920x1080
set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
BLENDER="${BLENDER:-blender}"
OUT="${OUT:-output}"
FPS="${FPS:-24}"

log() { printf '\033[1;35m[blender]\033[0m %s\n' "$*" >&2; }

command -v "$BLENDER" >/dev/null 2>&1 || { log "ERROR: blender not found; set BLENDER=/path/to/blender"; exit 1; }

ver="$("$BLENDER" --version 2>/dev/null | head -1 || true)"
log "using $ver"
case "$ver" in
  "Blender "[5-9]*|"Blender "[1-9][0-9]*) : ;;   # >= 5
  *) log "WARNING: Blender 5+ recommended; temperature lights may be unavailable." ;;
esac

# Default to animation on the GPU; forward any extra flags to render.py.
mode="animation"
args=("$@")
for i in "${!args[@]}"; do
  [[ "${args[$i]}" == "--mode" ]] && mode="${args[$((i+1))]:-animation}"
done

log "rendering on GPU -> $OUT"
"$BLENDER" -b -P "$HERE/render.py" -- --device GPU --out "$OUT" "${args[@]}"

if [[ "$mode" == "animation" ]]; then
  if command -v ffmpeg >/dev/null 2>&1; then
    "$HERE/encode.sh" "$OUT" "$OUT/render.mp4" "$FPS"
    log "wrote $OUT/render.mp4"
  else
    log "WARNING: ffmpeg not found; PNG frames are in $OUT (skipping MP4)."
  fi
fi
