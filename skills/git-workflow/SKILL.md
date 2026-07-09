---
name: git-workflow
description: Commit-early git discipline — commit and push working changes before running extensive or long tests so work is never lost to a crash, timeout, or exhausted budget. Use during any implementation task involving nontrivial changes followed by testing.
---

# git-workflow

**Commit and push before extensive testing.** Long test runs, big builds, and
Docker rebuilds can crash the session or exhaust the budget. A committed,
pushed checkpoint means work survives.

## The rule

1. Make a coherent, working change.
2. **Commit and push it** with a clear message — *before* kicking off extensive
   testing, benchmarks, or long builds.
3. Then test. If tests reveal fixes, commit those as follow-ups.

```sh
git add -A
git commit -m "Add X (pre-test checkpoint)"
git push -u origin <branch>
# now run the long test suite / docker build / benchmark
```

## Guidelines
- Prefer small, frequent commits over one large one.
- Push after each meaningful commit — local commits don't survive a lost
  container.
- Write descriptive messages (what and why), imperative mood.
- Never force-push shared branches without a `--force-with-lease` and a reason.
- Don't gate the checkpoint commit on tests passing; that's the whole point —
  checkpoint first, then test, then fix.

## Why "before" and not "after"
Testing is the risky, expensive step. If it hangs or the budget runs out
mid-run, an already-pushed checkpoint loses nothing. Committing only after tests
pass risks losing everything at the moment failure is most likely.
