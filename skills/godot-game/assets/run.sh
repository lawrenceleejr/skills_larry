#!/usr/bin/env bash
# Export a Godot game. Uses Docker (rebuilding the image only when the Dockerfile
# changes) with a host fallback when Godot is installed.
#   ./run.sh web            # export HTML5 -> build/web/
#   ./run.sh linux          # -> build/linux/
#   ./run.sh windows        # -> build/windows/
#   ./run.sh mac            # -> build/mac/
#   ./run.sh all            # every platform
#   FORCE_HOST=1 ./run.sh web
set -euo pipefail

cd "$(dirname "$0")"

IMAGE="${IMAGE:-godot-export:local}"
HASH_FILE=".docker-build-hash"
GODOT="${GODOT:-godot}"

log() { printf '\033[1;32m[godot]\033[0m %s\n' "$*" >&2; }

# preset name (as in export_presets.cfg) -> output file
declare -A PRESET=( [web]="Web" [linux]="Linux/X11" [windows]="Windows Desktop" [mac]="macOS" )
declare -A OUTFILE=( [web]="build/web/index.html" [linux]="build/linux/game.x86_64" \
                     [windows]="build/windows/game.exe" [mac]="build/mac/game.zip" )

export_one() {  # $1 = target key; runs the actual godot export (host or in-container)
  local key="$1" out="${OUTFILE[$1]}"
  mkdir -p "$(dirname "$out")"
  log "exporting '$key' -> $out"
  "$GODOT" --headless --import .              # ensure resources are imported
  "$GODOT" --headless --export-release "${PRESET[$key]}" "$out"
}

run_targets() {  # runs on host or already inside container
  local targets=("$@")
  [[ "${targets[0]}" == "all" ]] && targets=(web linux windows mac)
  for t in "${targets[@]}"; do
    [[ -n "${PRESET[$t]:-}" ]] || { log "unknown target: $t"; exit 2; }
    export_one "$t"
  done
}

need_rebuild() {
  [[ "${FORCE_REBUILD:-0}" == "1" ]] && return 0
  docker image inspect "$IMAGE" >/dev/null 2>&1 || return 0
  [[ -f "$HASH_FILE" ]] || return 0
  [[ "$(cat "$HASH_FILE")" != "$1" ]]
}

main() {
  local targets=("${@:-web}")
  if [[ "${IN_CONTAINER:-0}" == "1" ]]; then
    run_targets "${targets[@]}"
  elif [[ "${FORCE_HOST:-0}" == "1" ]] || ! command -v docker >/dev/null 2>&1; then
    command -v "$GODOT" >/dev/null 2>&1 || { log "ERROR: godot not found; set GODOT=... or use Docker."; exit 1; }
    log "running on host ($("$GODOT" --version 2>/dev/null | head -1))"
    run_targets "${targets[@]}"
  else
    local h; h="$(sha256sum Dockerfile | awk '{print $1}')"
    if need_rebuild "$h"; then
      log "building $IMAGE"
      DOCKER_BUILDKIT=1 docker build -t "$IMAGE" .
      printf '%s' "$h" > "$HASH_FILE"
    fi
    # The image entrypoint is `godot --headless`; re-enter this script instead.
    docker run --rm -v "$PWD:/project" -w /project -e IN_CONTAINER=1 \
      --entrypoint bash "$IMAGE" ./run.sh "${targets[@]}"
  fi
}

main "$@"
