---
name: audit-loop
description: Before declaring any task done, run a critical audit loop over the repository/change — actively hunt for bugs, gaps, and improvements, verify findings, fix what matters, and repeat until clean. Use at the end of every task and whenever reviewing a repo, change, or design.
---

# audit-loop

Never stop at "it works." On **every** task, run an audit loop: critically think
through the repo/change, find issues, suggest and apply improvements, then
re-audit until it's clean.

## The loop
1. **Survey.** Re-read the actual change/repo with fresh, skeptical eyes. State
   what it's supposed to do vs. what it does.
2. **Hunt** across these dimensions (see `references/checklist.md`):
   correctness, edge cases, error handling, security, reproducibility, tests,
   CI, docs, consistency, performance, and dead/duplicate code.
3. **Verify each finding.** Reproduce it or trace the code path — don't report
   speculation. Rank by severity.
4. **Fix what matters** now; record the rest as explicit follow-ups (issues or
   a TODO), never silently.
5. **Re-run checks** (lint, tests, shellcheck, the actual command) after fixes.
6. **Repeat** until a pass surfaces nothing material. Then summarize what you
   found and what you changed.

## Rules
- Be adversarial about your *own* work — assume there's a bug and go find it.
- Prefer verifying by *running* things over reasoning alone (build, test,
  execute, render, inspect artifacts).
- One finding = one clear statement of the failure scenario (inputs → wrong
  result), not a vague worry.
- Don't hide caps or shortcuts; surface them.
- Distinguish **blocking** (must fix) from **nice-to-have** (suggest).

## Output
End with a short audit summary: issues found (with severity), fixes applied,
and remaining suggestions. If nothing material remains, say so plainly.

For repo-wide audits, `references/checklist.md` is the dimension list to sweep.
