---
name: desktop-app
description: Build desktop applications in CI and publish a downloadable artifact (and release asset) so the binary can be fetched from GitHub. Use when building any GUI/desktop app (Electron, Tauri, PyInstaller, Qt, etc.).
---

# desktop-app

When building a desktop app, **build it in CI and upload a downloadable
artifact** so I can grab the binary from GitHub without building locally.

## Requirements
1. CI builds the app on every push (at least on the default branch).
2. The built binary is uploaded via `actions/upload-artifact` — downloadable
   from the run summary.
3. On tagged releases, also attach the binary as a release asset.
4. Build for the target OS(es) with a matrix when cross-platform.

## Drop-in workflow
`assets/desktop-build.yml` builds across a matrix and uploads artifacts. Adapt
the `build` step to your toolchain:

- **Electron:** `npm ci && npm run make` (electron-forge) or `electron-builder`.
- **Tauri:** `tauri-apps/tauri-action` (also handles release assets).
- **Python:** `pyinstaller --onefile app.py` → artifact in `dist/`.

```sh
mkdir -p .github/workflows
cp skills/desktop-app/assets/desktop-build.yml .github/workflows/desktop-build.yml
```

## Notes
- Name artifacts by OS + arch so downloads are unambiguous.
- Keep the artifact retention long enough to be useful (`retention-days`).
- Code-sign/notarize in CI for macOS/Windows when distributing widely (store
  certs as encrypted secrets).
- Prefer building in Docker where the toolchain allows, for reproducibility
  (see `docker-run`); some GUI toolchains need the native runner.
