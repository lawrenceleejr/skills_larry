---
name: ci-testing
description: Set up GitHub Actions CI that runs the test suite on every push and pull request, and publishes the project's Docker image to the GitHub Container Registry (GHCR). Use when creating a new repo or adding CI to an existing one.
---

# ci-testing

Every repo gets CI that (1) tests on every push and PR, and (2) publishes the
Docker image to GHCR.

## Drop-in workflow

Copy `assets/ci.yml` to `.github/workflows/ci.yml` and adjust the test command.

```sh
mkdir -p .github/workflows
cp skills/ci-testing/assets/ci.yml .github/workflows/ci.yml
```

It has two jobs:

- **test** — checks out, sets up the environment, and runs the suite. Prefer
  reusing the project's `run.sh` (`./run.sh test`) so CI and local behavior
  match (see `docker-run`).
- **publish** — builds and pushes `ghcr.io/<owner>/<repo>` on pushes to the
  default branch. Uses `GITHUB_TOKEN` with `packages: write`; no extra secrets.

## Principles
- **Test on every push and PR.** No exceptions; a broken push should go red.
- **Fail fast, cache well.** Cache dependency and Docker layers.
- **One source of truth.** CI calls the same entrypoint developers use.
- **Least privilege.** Only the publish job gets `packages: write`.

## GHCR notes
- Image name is lowercase `ghcr.io/${{ github.repository }}`.
- Log in with `docker/login-action` using `${{ github.actor }}` /
  `${{ secrets.GITHUB_TOKEN }}`.
- Tag with both `latest` and the commit SHA.
- To make the package public, set its visibility in the repo's Packages
  settings after the first push.

See `references/notes.md` for matrix builds, caching, and required-check setup.
