# Working conventions

Follow these in every project. The `skills/` directory expands on each point.

1. **Dockerize the work.** Put builds, tests, and analyses in a Docker image
   driven by a `run.sh`. The script rebuilds the image only when source changed
   (hash-based marker) and falls back to the host when deps are available
   (`FORCE_HOST=1`). See `skills/docker-run`.
2. **Commit and push before extensive testing.** Never risk losing work to a
   crash or an exhausted budget. See `skills/git-workflow`.
3. **CI tests every push.** See `skills/ci-testing`.
4. **Publish Docker images to GHCR** (`ghcr.io/<owner>/<repo>`).
5. **Plots:** Tufte principles, single panel per file, **PDF** output. See
   `skills/tufte-plots`.
6. **HEP I/O:** use `uproot`, not PyROOT, when possible. See
   `skills/uproot-analysis`.
7. **Desktop apps:** build in CI, upload a downloadable artifact. See
   `skills/desktop-app`.
8. Keep responses concise.
