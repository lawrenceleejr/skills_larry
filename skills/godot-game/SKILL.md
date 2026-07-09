---
name: godot-game
description: Build interactive games with Godot (4.x) in Docker by default unless another engine is specified, export for all common platforms (Linux, Windows, macOS, Web) in CI, and deploy the web build to GitHub Pages from main only when it runs in a browser successfully. Use for any game or interactive-simulation project.
---

# godot-game

Default game engine is **Godot 4.x**, run **in Docker**. Use another engine only
when the user specifies one. Build in CI for all common platforms and publish
the web build to GitHub Pages when it actually runs in a browser.

## Setup
Copy the assets to the game repo root, then export via `run.sh`:
```sh
cp skills/godot-game/assets/{Dockerfile,run.sh,export_presets.cfg,smoke_web.py} .
mkdir -p .github/workflows
cp skills/godot-game/assets/ci.yml .github/workflows/game.yml
```
Keep `project.godot` and `export_presets.cfg` at the repo root. Regenerate
`export_presets.cfg` from Godot's editor (Project → Export) if options drift; the
preset **names** must stay `Web`, `Linux/X11`, `Windows Desktop`, `macOS`.

## Exporting
```sh
./run.sh web              # HTML5 -> build/web/
./run.sh linux|windows|mac
./run.sh all              # every platform
FORCE_HOST=1 ./run.sh web # use a locally installed Godot instead of Docker
```
`run.sh` rebuilds the image only when the Dockerfile changes (see `docker-run`).
The image bundles headless Godot **and** matching export templates (versions must
match exactly).

## CI (`ci.yml`)
1. **build** — builds the Docker image and exports all platforms; uploads desktop
   builds and the web build as downloadable artifacts.
2. **smoke-web** — serves the web export the way Pages will (plain HTTP, no
   COOP/COEP) and loads it in headless Chromium via `smoke_web.py`, asserting the
   engine initializes without fatal errors.
3. **deploy-pages** — publishes the web build to GitHub Pages **only** on the
   default branch **and only if the smoke test passed**. In the repo, set
   Settings → Pages → Source: GitHub Actions.

## Web / GitHub Pages gotcha
Pages doesn't send COOP/COEP headers, so `SharedArrayBuffer` (Godot's threaded
web build) won't work. The preset sets `threads/thread_support=false` so the
build runs on Pages. If you need threads, self-host with the right headers or use
a `coi-serviceworker` shim (see `references/notes.md`).

## Other engines
If the user specifies Unity/Unreal/Bevy/etc., follow that instead — but keep the
same shape: Dockerized where feasible, CI builds for all common platforms,
downloadable artifacts, and a gated web deploy when a browser build exists.

Always run the `audit-loop`, and use the visual/interactive inspection habit:
actually launch the exported build and confirm it plays.
