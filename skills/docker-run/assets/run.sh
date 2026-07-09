#!/usr/bin/env bash
# Reproducible run script: runs the workload in Docker, rebuilding the image only
# when build inputs change. Falls back to the host when Docker is unavailable or
# FORCE_HOST=1 is set.
set -euo pipefail

cd "$(dirname "$0")"

# ---- configure -------------------------------------------------------------
IMAGE="${IMAGE:-ghcr.io/OWNER/REPO:latest}"   # set to your GHCR path
HASH_INPUTS=(Dockerfile requirements.txt src) # inputs that trigger a rebuild
HASH_FILE=".docker-build-hash"
# Command that must succeed for the host fallback to be permitted:
HOST_CHECK() { command -v python3 >/dev/null && python3 -c "import sys"; }
# The workload. Identical in Docker and on the host. "$@" are passed through.
run_workload() { python3 src/main.py "$@"; }
# ---------------------------------------------------------------------------

log() { printf '\033[1;34m[run]\033[0m %s\n' "$*" >&2; }

compute_hash() {
  # Hash the contents of all existing HASH_INPUTS deterministically.
  local existing=()
  for p in "${HASH_INPUTS[@]}"; do [[ -e "$p" ]] && existing+=("$p"); done
  # find keeps output stable; sort for order-independence.
  find "${existing[@]}" -type f -exec sha256sum {} + 2>/dev/null \
    | sort | sha256sum | awk '{print $1}'
}

need_rebuild() {
  local current="$1"
  [[ "${FORCE_REBUILD:-0}" == "1" ]] && return 0
  docker image inspect "$IMAGE" >/dev/null 2>&1 || return 0
  [[ -f "$HASH_FILE" ]] || return 0
  [[ "$(cat "$HASH_FILE")" != "$current" ]]
}

run_in_docker() {
  local current; current="$(compute_hash)"
  if need_rebuild "$current"; then
    log "building $IMAGE (source changed)"
    DOCKER_BUILDKIT=1 docker build -t "$IMAGE" .
    printf '%s' "$current" > "$HASH_FILE"
  else
    log "reusing $IMAGE (no source change)"
  fi
  docker run --rm -v "$PWD:/work" -w /work "$IMAGE" "$@"
}

run_on_host() {
  log "running on host"
  if ! HOST_CHECK; then
    log "ERROR: host dependencies missing; install them or run with Docker."
    exit 1
  fi
  run_workload "$@"
}

main() {
  if [[ "${FORCE_HOST:-0}" == "1" ]] || ! command -v docker >/dev/null 2>&1; then
    run_on_host "$@"
  else
    # When invoked inside the container, IN_CONTAINER=1 runs the workload directly.
    if [[ "${IN_CONTAINER:-0}" == "1" ]]; then run_workload "$@"; else run_in_docker "$@"; fi
  fi
}

main "$@"
