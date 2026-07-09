# Static site notes

## Why a generator (not hand-rolled HTML)
Content in Markdown, layouts/themes reused, fast incremental builds, and a
well-trodden deploy path. Hugo is a single Go binary — trivial in Docker and CI.

## Hugo essentials
- Config: `hugo.toml` (or `config/`). Set `baseURL`, `title`, `theme`.
- Content: `content/`. New page: `hugo new posts/my-post.md`.
- Themes: add as a git submodule under `themes/` and set `theme = "..."`.
- Output: `public/` (gitignored).

## Jekyll alternative
GitHub Pages builds Jekyll natively, but prefer the Actions flow for control.
- `Gemfile` with `gem "jekyll"`; build with `bundle exec jekyll build -d public`.
- Docker: `FROM ruby:3.3-slim`, `bundle install`, `jekyll build`.
- Reuse the same `pages.yml` shape: build job produces `public/`, deploy job
  publishes on `main`.

## GitHub Pages deploy
- Set Settings → Pages → Source: **GitHub Actions** (not "deploy from branch").
- The `deploy` job needs `pages: write` and `id-token: write`.
- `actions/configure-pages` outputs the correct `base_url` — pass it to the
  build so links work for both `user.github.io` and project (`/repo/`) sites.
- Only `main` deploys; PRs/other branches build as a check but don't publish.

## Custom domain
Add a `CNAME` file (via `static/CNAME`) and configure DNS; set it in Pages
settings. Keep `baseURL` consistent with the domain.
