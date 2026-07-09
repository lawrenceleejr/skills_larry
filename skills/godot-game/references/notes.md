# Godot / game build notes

## Version pinning
- The Docker `GODOT_VERSION`/`GODOT_RELEASE` build args pin the engine, and the
  export templates in the image **must match** exactly (`4.3.stable` etc.).
  Mismatched templates fail the export.
- Bump both together; rebuild the image (the run script rebuilds on Dockerfile
  change).

## Import step
Exports need imported resources. `run.sh` runs `godot --headless --import .`
before exporting so a clean checkout (no `.godot/`) exports correctly. Keep
`.godot/` out of git.

## Web export on GitHub Pages
- Pages serves static files without `Cross-Origin-Opener-Policy` /
  `Cross-Origin-Embedder-Policy`, so `SharedArrayBuffer` is blocked and a
  thread-enabled Godot web build won't boot. Hence `threads/thread_support=false`.
- Want threads anyway? Options:
  - Self-host (Netlify/Cloudflare/nginx) and send COOP: `same-origin` +
    COEP: `require-corp`.
  - Add a `coi-serviceworker.js` shim that reloads the page with those headers
    client-side (works on Pages, with caveats on first load / Safari).
- The `smoke_web.py` gate serves the build exactly like Pages (no special
  headers) so a green smoke test means it will actually run once deployed.

## Platforms
- Linux `.x86_64`, Windows `.exe`, macOS `.zip` (app bundle), Web (`index.html`
  + `.wasm`/`.pck`/`.js`).
- macOS notarization/signing needs Apple credentials; unsigned builds run with a
  Gatekeeper prompt. Sign in CI with secrets when distributing.
- Windows code signing similarly optional but recommended for distribution.

## Inspecting
Don't trust "export succeeded" — run the desktop build and play the web artifact
locally (`python -m http.server` in `build/web`) before trusting a release. CI's
browser smoke test is the automated backstop.

## Other engines
Bevy (Rust) → `wasm-bindgen` + `trunk` for web, `cargo` per-target for desktop.
Unity/Unreal → their CLI batch-build; both Dockerize with more effort. Keep the
CI shape identical: all-platform artifacts + gated web deploy.
