# CI notes

## Matrix builds
Test across versions when it matters:
```yaml
strategy:
  matrix:
    python-version: ["3.11", "3.12"]
```

## Caching
- `actions/setup-python` with `cache: pip` caches wheels.
- For Docker, `cache-from/to: type=gha` uses the Actions cache backend.
- Cache large data fixtures with `actions/cache` keyed on a content hash.

## Required checks
In repo settings → Branches → protect the default branch and mark the `test`
job as a required status check so red pushes can't merge.

## Publishing
- `GITHUB_TOKEN` needs `packages: write` (set at job level, not workflow).
- Tag `latest` + commit SHA; add semver tags on release with
  `docker/metadata-action`.
- First GHCR push creates a private package; change visibility in Packages
  settings to make it public.

## Artifacts
Use `actions/upload-artifact` to expose build outputs (e.g. generated PDFs,
desktop binaries) for download from the run summary. See `desktop-app`.
