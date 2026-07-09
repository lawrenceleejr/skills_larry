#!/usr/bin/env bash
# Encode a PNG frame sequence into an MP4 with ffmpeg.
#   ./encode.sh <frames_dir> [out.mp4] [fps]
set -euo pipefail

DIR="${1:?usage: encode.sh <frames_dir> [out.mp4] [fps]}"
OUT="${2:-$DIR/render.mp4}"
FPS="${3:-24}"

command -v ffmpeg >/dev/null 2>&1 || { echo "ffmpeg not found" >&2; exit 1; }

# Blender writes frame_0001.png, frame_0002.png, ...
first="$(find "$DIR" -maxdepth 1 -name 'frame_*.png' | sort | head -1)"
[[ -n "$first" ]] || { echo "no frame_*.png in $DIR" >&2; exit 1; }
# Extract the frame number portably (BSD/macOS sed lacks \+): digits only,
# then strip leading zeros via base-10 arithmetic.
digits="$(basename "$first" | tr -dc '0-9')"
start="$((10#$digits))"

ffmpeg -y -framerate "$FPS" -start_number "$start" \
  -i "$DIR/frame_%04d.png" \
  -c:v libx264 -pix_fmt yuv420p -crf 18 -movflags +faststart \
  "$OUT"
echo "wrote $OUT"
