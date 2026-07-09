---
name: static-site
description: Build websites with an established static site generator (Hugo by default, Jekyll alternative), buildable in a Docker image, with GitHub Actions CI that builds every push and deploys to GitHub Pages from the main branch. Use whenever building or deploying a website, docs site, blog, or landing page.
---

# static-site

Don't hand-roll a site. Use an established static site generator and let CI
build and deploy it.

- **Generator:** Hugo by default (single binary, fast, trivial to Dockerize).
  Jekyll is the supported alternative — see `references/notes.md`.
- **Buildable in Docker:** `assets/Dockerfile` + `assets/run.sh` build/serve in
  a container, with a host fallback when the tool is installed.
- **CI builds every push.** `assets/pages.yml` builds on every push/PR.
- **Deploy to GitHub Pages from `main`.** Only the default branch deploys;
  other branches build (as a check) but don't publish.

## Setup
```sh
# New Hugo site (once):
hugo new site . --force            # or run it via ./run.sh

mkdir -p .github/workflows
cp skills/static-site/assets/Dockerfile .
cp skills/static-site/assets/run.sh .
cp skills/static-site/assets/pages.yml .github/workflows/pages.yml
```

Then in the repo: Settings → Pages → **Source: GitHub Actions**.

## Build & preview
```sh
./run.sh build            # in Docker; outputs to ./public
./run.sh serve            # live-reload dev server on :1313
FORCE_HOST=1 ./run.sh build   # on the host if hugo is installed
```
`run.sh` rebuilds the image only when the Dockerfile changes (see `docker-run`).

## CI / deploy (`pages.yml`)
- Builds with Hugo extended, sets the correct `--baseURL` for Pages.
- Uploads the `public/` artifact.
- A `deploy` job publishes to Pages **only on `main`** using the official
  `actions/deploy-pages` flow (`pages: write`, `id-token: write`).

## Notes
- Set `baseURL` in `hugo.toml`; CI overrides it with the Pages URL at build time.
- Pin the generator version (build arg / workflow input) for reproducibility.
- Commit `public/` to `.gitignore` — it's a build output.
- For a project site the base path is `/<repo>/`; the workflow handles this.
