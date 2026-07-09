---
name: plan-then-delegate
description: Plan complex work on a powerful model in plan mode, writing an explicit step-by-step implementation spec aimed at a weaker model, then suggest the user drop to a cheaper model and execute the steps via a series of subagents. Use at the start of any non-trivial, multi-step implementation task where planning quality matters but per-step execution is mechanical.
---

# plan-then-delegate

Use the strong model's judgment where it pays off — **planning** — then hand the
mechanical **execution** to cheaper models running as subagents.

## When to use
Non-trivial, multi-step tasks where the hard part is deciding *what* to do, and
each individual step is straightforward once specified. Skip it for quick
one-off edits (just do them) or for work that needs strong reasoning in every
step (stay on the powerful model throughout).

## Workflow

### 1. Plan on the powerful model, in plan mode
- Ensure you're on a capable model (e.g. Opus). Enter **plan mode**
  (`EnterPlanMode`) so no edits happen while planning.
- Research the codebase thoroughly: read the relevant files, find conventions,
  identify risks and dependencies. Ask clarifying questions
  (`AskUserQuestion`) when a decision is genuinely the user's.

### 2. Write the plan *for a weaker model*
Assume the implementer cannot infer intent. Each step must be **atomic,
ordered, and unambiguous** — see `references/plan-template.md`. Every step
states: the goal, exact files/symbols, the concrete change, commands to run, and
an **acceptance check** the implementer can verify without judgment. Front-load
shared context (conventions, gotchas) so steps don't rely on hidden knowledge.

### 3. Present the plan and suggest dropping the model
- `ExitPlanMode` to present the plan for approval.
- Then explicitly suggest: *"This plan is mechanical to execute — you can switch
  to a cheaper model (e.g. `/model sonnet` or `/model haiku`) for
  implementation to save cost/time. I'll drive it with subagents."* Let the user
  decide.

### 4. Execute via a series of subagents
- Spawn one subagent per step (or per independent group), passing that step's
  full spec from the plan. Use `Agent` (or `Task`) with a lower `model`.
- **Independent steps** → launch in parallel. **Dependent steps** → sequential,
  feeding results forward.
- After each step, verify the acceptance check before proceeding. Commit and
  push at checkpoints (see `git-workflow`).
- Keep the orchestration (deciding order, checking results, handling surprises)
  on yourself; only the well-specified execution goes to the cheaper subagents.

## Rules
- A step a weaker model can't do unambiguously is under-specified — refine it,
  don't delegate the ambiguity.
- If a subagent hits something the plan didn't cover, stop and re-plan on the
  strong model rather than letting the cheap model improvise.
- End with the `audit-loop` skill over the combined result.

See `references/plan-template.md` for the step format and a delegation checklist.
