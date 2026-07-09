#!/usr/bin/env bash
# Run the example workload reproducibly.
#   ./run.sh            -> generate the PDF plot (in Docker, rebuild if changed)
#   ./run.sh test       -> run the test suite
#   FORCE_HOST=1 ./run.sh [...]  -> run on the host if deps are available
set -euo pipefail

EXAMPLE_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$EXAMPLE_DIR/.." && pwd)"

IMAGE="${IMAGE:-ghcr.io/lawrenceleejr/skills_larry:latest}"
HASH_FILE="$EXAMPLE_DIR/.docker-build-hash"
# Inputs that should trigger a rebuild (relative to repo root).
HASH_INPUTS=(example/Dockerfile example/requirements.txt example/src example/run.sh skills/tufte-plots/assets)

log() { printf '\033[1;34m[run]\033[0m %s\n' "$*" >&2; }

host_deps_ok() {
  python3 - <<'PY' >/dev/null 2>&1
import importlib
for m in ("uproot", "awkward", "numpy", "hist", "matplotlib"):
    importlib.import_module(m)
PY
}

# The workload — identical in Docker and on the host.
run_workload() {
  if [[ "${1:-}" == "test" ]]; then
    exec python3 -m pytest -q "$EXAMPLE_DIR/tests"
  fi
  exec python3 "$EXAMPLE_DIR/src/main.py" "$@"
}

compute_hash() {
  cd "$REPO_ROOT"
  local existing=()
  for p in "${HASH_INPUTS[@]}"; do [[ -e "$p" ]] && existing+=("$p"); done
  # No inputs present: emit a constant so `find` doesn't default to hashing "."
  [[ ${#existing[@]} -eq 0 ]] && { printf 'no-inputs'; return; }
  find "${existing[@]}" -type f -exec sha256sum {} + 2>/dev/null | sort | sha256sum | awk '{print $1}'
}

need_rebuild() {
  [[ "${FORCE_REBUILD:-0}" == "1" ]] && return 0
  docker image inspect "$IMAGE" >/dev/null 2>&1 || return 0
  [[ -f "$HASH_FILE" ]] || return 0
  [[ "$(cat "$HASH_FILE")" != "$1" ]]
}

run_in_docker() {
  local current; current="$(compute_hash)"
  if need_rebuild "$current"; then
    log "building $IMAGE (source changed)"
    DOCKER_BUILDKIT=1 docker build -f "$EXAMPLE_DIR/Dockerfile" -t "$IMAGE" "$REPO_ROOT"
    printf '%s' "$current" > "$HASH_FILE"
  else
    log "reusing $IMAGE (no source change)"
  fi
  docker run --rm -v "$REPO_ROOT:/work" -w /work/example "$IMAGE" "$@"
}

main() {
  if [[ "${IN_CONTAINER:-0}" == "1" ]]; then
    run_workload "$@"
  elif [[ "${FORCE_HOST:-0}" == "1" ]] || ! command -v docker >/dev/null 2>&1; then
    if ! host_deps_ok; then
      log "ERROR: host deps missing (pip install -r requirements.txt) or use Docker."
      exit 1
    fi
    log "running on host"
    run_workload "$@"
  else
    run_in_docker "$@"
  fi
}

main "$@"
