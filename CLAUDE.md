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
8. **Websites:** use Hugo/Jekyll, build in Docker, CI builds every push, deploy
   to GitHub Pages from `main`. See `skills/static-site`.
9. **Games:** Godot in Docker by default, CI builds all platforms, gated Web
   deploy to Pages. See `skills/godot-game`.
10. **Typography:** free Google Fonts, self-hosted; apply pairing & hierarchy
    principles. See `skills/typography`.
11. **Blender:** warm soft temperature lighting, enclosing sphere, wide-angle
    DOF + motion blur, animated cameras, host-GPU or Docker/CI. See
    `skills/blender-render`.
12. **Progress bars for long processes.** Any tool that can run longer than a
    few seconds shows a useful progress bar — fraction done, rate, ETA
    (`tqdm` in Python; heartbeat log lines in CI/non-TTY). See
    `skills/progress-bars`.
13. **Audit everything.** End every task with a critical audit loop; verify and
    fix before declaring done. See `skills/audit-loop`.
14. **Plan high, execute low.** For big tasks, plan on a strong model then
    delegate explicit steps to cheaper subagents. See `skills/plan-then-delegate`.
15. Keep responses concise.
