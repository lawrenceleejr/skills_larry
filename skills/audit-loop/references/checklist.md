# Audit checklist

Sweep every dimension; for each, ask "how does this break?"

## Correctness
- Off-by-one, wrong defaults, inverted conditions, wrong units.
- Does the code do what the docs/name claim?
- Boundary values: empty, zero, one, huge, negative, unicode, NaN.

## Error handling
- What happens when inputs are missing, malformed, or a dependency is absent?
- Are failures loud (non-zero exit, clear message) or silent?
- `set -euo pipefail` in shell; no swallowed exceptions.

## Reproducibility
- Pinned versions (images, tools, deps)? No `latest` where it bites.
- Same entrypoint locally and in CI?
- Deterministic outputs; no reliance on ambient host state.

## Security
- Secrets not committed; least-privilege CI tokens (`packages`/`pages` only
  where needed).
- No untrusted input executed; no `curl | bash` from unpinned sources.
- Non-root containers.

## Tests & CI
- Do tests actually assert behavior (not just "runs")?
- Does CI run on every push/PR and gate merges?
- Are artifacts produced and downloadable where promised?
- Are all scripts linted (shellcheck) and code checked?

## Docs & consistency
- README/skill descriptions match what the code does.
- Naming, style, and conventions consistent across the repo.
- Examples actually run.

## Performance & waste
- Unnecessary rebuilds; missing caches.
- Duplicated logic that should be shared.
- Dead code, unused files.

## Repo hygiene
- `.gitignore` covers build outputs/caches (and isn't over-broad — beware
  negations like `!skills/**` that un-ignore `__pycache__`).
- No stray generated files tracked.

## Severity
- **Blocking:** wrong results, data loss, broken build/deploy, security hole.
- **Major:** missing tests for core paths, silent failure, poor reproducibility.
- **Minor / nice-to-have:** style, docs polish, small perf wins.
