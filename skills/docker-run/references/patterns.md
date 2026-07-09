# Docker run-script patterns

## Change detection
- Hash *contents*, not mtimes — mtimes change on checkout and break caching.
- Include every file that affects the image: Dockerfile, lockfiles, and source
  that is `COPY`ed in. Exclude outputs and caches.
- Store the marker (`.docker-build-hash`) in `.gitignore`.

## Layer caching
- Copy dependency manifests and install *before* copying source, so editing
  source doesn't invalidate the dependency layer.
- Use `DOCKER_BUILDKIT=1` for parallelism and better caching.

## Host fallback
- `HOST_CHECK` should verify the *actual* interpreter/tools and importable
  libraries, not just that a binary exists.
- Keep `run_workload` free of Docker-only assumptions (paths, users) so it works
  identically on the host.

## CI
- In CI, prefer `docker buildx` with a registry cache (`--cache-from`,
  `--cache-to`) so builds are fast across runs.
- Reuse the same `run.sh` in CI as locally — do not duplicate the command.

## Non-root
- Run as a non-root user in the image. Mount the workdir with matching
  permissions, or write outputs to a world-writable path.
