---
name: docker-run
description: Dockerize builds, tests, and analyses behind a run script that rebuilds the image only when source changes and falls back to running on the host when dependencies are available. Use when setting up a new project, adding a reproducible run/test entrypoint, or when the user wants work done "in Docker" or asks for a run script.
---

# docker-run

Do as much work as possible inside a Docker image, driven by a `run.sh`.

## Requirements the run script must meet

1. **Rebuild only on change.** Hash the build inputs (Dockerfile + tracked
   source that affects the image, e.g. `requirements.txt`, `pyproject.toml`,
   `src/`). Store the hash in a marker file. Rebuild only when the hash differs
   or the image is missing.
2. **Host fallback.** If Docker is unavailable, or `FORCE_HOST=1` is set, run
   the same command on the host — provided required deps are present. Detect
   missing deps and fail with a clear message.
3. **Same entrypoint both ways.** Docker and host paths run the *same* command
   so behavior is identical.

## Use the template

`assets/run.sh` is a ready-to-adapt implementation. Copy it next to a
`Dockerfile`, set the variables at the top, and edit `run_workload`.

```sh
cp skills/docker-run/assets/run.sh   ./run.sh
cp skills/docker-run/assets/Dockerfile ./Dockerfile
```

Key knobs in `run.sh`:

- `IMAGE` — image name (use `ghcr.io/<owner>/<repo>` so CI can push it).
- `HASH_INPUTS` — files/dirs whose contents should trigger a rebuild.
- `HOST_CHECK` — command that must succeed for the host fallback to be allowed.
- `run_workload()` — the actual command; identical in both modes.

## How the change detection works

The script computes `sha256` over `HASH_INPUTS` and compares it to
`.docker-build-hash`. Matching hash + existing image ⇒ skip the build. This
makes repeated runs fast while staying correct when you edit the Dockerfile or
dependencies.

See `references/patterns.md` for edge cases (CI caching, multi-stage builds,
BuildKit, non-root users).
