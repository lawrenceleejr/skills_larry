# Plan template & delegation checklist

The plan is a contract a weaker model executes literally. Write it so success is
unambiguous and verifiable.

## Shared context (once, at the top)
- **Goal:** one sentence on the end state.
- **Conventions:** style, naming, patterns to match (with example file paths).
- **Constraints & gotchas:** anything non-obvious that would trip an implementer.
- **Global acceptance:** how we know the whole task is done (tests pass, CI green,
  command produces expected output).

## Per-step format
```
### Step N — <imperative title>
- Depends on: <step numbers, or "none">
- Files: <exact paths / symbols to touch>
- Change: <the specific edit, precisely enough to apply without guessing>
- Commands: <exact commands to run>
- Acceptance: <objective check — command exits 0 / file contains X / test passes>
- If it fails: <fallback, or "stop and report">
```

### A good step
- Atomic: one coherent change; no "and also…".
- Ordered: dependencies explicit so parallelizable steps are obvious.
- Verifiable without judgment: the acceptance check is mechanical.
- Self-contained: names the files and includes needed context; no "you know
  what I mean".

### A bad step (don't do this)
- "Refactor the module to be cleaner." (subjective, unbounded)
- "Fix the tests." (which? how do you know they're fixed?)
- "Update the relevant files." (which files?)

## Delegation checklist
- [ ] On a powerful model + plan mode while planning.
- [ ] Codebase researched; decisions that are the user's were asked.
- [ ] Every step atomic, ordered, with a mechanical acceptance check.
- [ ] Shared context front-loaded so steps don't need hidden knowledge.
- [ ] Plan presented via ExitPlanMode; model-downgrade suggested to the user.
- [ ] Independent steps parallelized; dependent steps sequential.
- [ ] Acceptance verified after each step; checkpoints committed & pushed.
- [ ] Surprises escalate back to the strong model, not improvised by subagents.
- [ ] audit-loop run over the final result.
