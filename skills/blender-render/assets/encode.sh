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
start="$(basename "$first" | sed 's/frame_0*\([0-9]\+\)\.png/\1/')"

ffmpeg -y -framerate "$FPS" -start_number "$start" \
  -i "$DIR/frame_%04d.png" \
  -c:v libx264 -pix_fmt yuv420p -crf 18 -movflags +faststart \
  "$OUT"
echo "wrote $OUT"
