# skills_larry

A collection of [Claude Code skills](https://code.claude.com/docs) encoding my
engineering best practices. Point Claude Code at this repo (as a plugin, or copy
`skills/` into `.claude/skills/`) and it will follow these conventions.

## Skills

| Skill | Purpose |
|-------|---------|
| [`docker-run`](skills/docker-run) | Dockerize work; run scripts that rebuild the image only when source changes, with a host fallback |
| [`ci-testing`](skills/ci-testing) | CI that tests on every push and publishes Docker images to GHCR |
| [`tufte-plots`](skills/tufte-plots) | Single-panel PDF plots following Tufte's principles |
| [`uproot-analysis`](skills/uproot-analysis) | Read ROOT files with `uproot`, not PyROOT |
| [`desktop-app`](skills/desktop-app) | Build desktop apps in CI and expose a downloadable artifact |
| [`git-workflow`](skills/git-workflow) | Commit and push before extensive testing |
| [`blender-render`](skills/blender-render) | Cinematic Blender renders: warm soft temperature lighting, enclosing sphere, wide-angle DOF + motion blur, animated cameras, host-GPU or Docker/CI, PNG→MP4 |

## Core principles

- **Reproducible by default.** Do as much as possible inside Docker images
  driven by run scripts. Scripts detect source changes and rebuild only when
  needed, and fall back to running on the host when dependencies are present.
- **Commit early.** Commit and push *before* extensive testing so work is never
  lost to a crash or an exhausted budget.
- **Test on every push.** Every repo ships CI that runs the test suite.
- **Publish images.** Docker images go to the GitHub Container Registry (GHCR).
- **Tufte plots.** Maximize data-ink, single panel per file, PDF output.
- **`uproot` over PyROOT** whenever the analysis allows.

## Example

`example/` is a working, self-testing demonstration: a dockerized `uproot` +
`matplotlib` environment that produces a Tufte-style single-panel PDF. The repo
CI exercises it on every push and publishes the image to GHCR.

```sh
./example/run.sh                # runs in Docker, rebuilding only if source changed
FORCE_HOST=1 ./example/run.sh   # runs on the host if deps are available
```
