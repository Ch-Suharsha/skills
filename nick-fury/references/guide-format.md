# Project build guide format

Use this structure for `docs/project-build-guide.md`. Adapt headings when needed,
but preserve the distinction between copy-paste prompts and teaching notes.

## Header

Include:

- project name;
- guide version or generated date when useful;
- current teaching mode: Guided, Collaborative, or Independent;
- link to `project-brief.md`;
- a reminder that checkboxes represent verified completion, not merely attempted work.

## Executive summary

Summarize the product, first useful release, selected stack, and the highest-risk
assumption in a few paragraphs.

## Product mind map

Create a Mermaid `mindmap` when the renderer supports it. Show users, core
workflows, major components, data, integrations, and delivery. Keep it conceptual
rather than listing every source file.

If Mermaid mind maps are unsupported, use a small indented tree.

## Build sequence

Create a compact table:

| # | Phase | Outcome | Depends on | Status |
|---|---|---|---|---|
| 1 | ... | ... | ... | ⬜ |

Status values may be `⬜ Not started`, `🟡 In progress`, `✅ Verified`, or
`⛔ Blocked`. A phase is verified only after its gate passes.

## Prompt section

Use this pattern for every dynamic phase:

````markdown
## Prompt N — Descriptive outcome

**Status:** ⬜ Not started  
**Depends on:** Prompt X or None  
**Produces:** Concrete files, behavior, or decision

### Copy-paste prompt

```text
[A directly usable prompt tailored to this project and phase.]
```

### Why this prompt now

[Explain its place in the dependency sequence.]

### How it helps the coding agent

[Explain what context, boundaries, or completion signal it provides.]

### Trade-offs

- **Gain:** ...
- **Cost or limitation:** ...
- **Deferred:** ...

### Expected result

[Describe observable deliverables.]

### Verify before continuing

- [ ] Exact test, command, inspection, or user confirmation.
- [ ] Evidence that failure and repeated execution behave correctly when relevant.

### What you are learning

[Explain the new concept in plain language.]

**Check yourself:** [One short question the learner should now answer.]
````

## Content of a copy-paste prompt

Use only the elements relevant to that phase, generally in this order:

1. Read the project brief and inspect current state.
2. State the single outcome.
3. List requirements and important exclusions.
4. Define acceptance criteria.
5. Require proportional verification.
6. Define the completion report.
7. State external-action boundaries.

Example shape, not mandatory wording:

```text
Read docs/project-brief.md and inspect the current repository before changing it.

Objective:
[One outcome.]

Requirements:
- ...

Constraints:
- Preserve unrelated changes.
- Do not hardcode secrets.

Acceptance criteria:
- ...

Verification:
- Run ...

Afterward, report what changed, how to run it, the relevant evidence, and any
remaining limitation. Do not commit, push, deploy, or perform other external
actions unless explicitly requested.
```

Avoid repeating the full architecture, stack, or requirements in every prompt;
the project brief is the shared context. Repeat a fact only when omitting it
would create a likely safety or correctness error.

## Checkpoints

After a vertical slice, major integration, and pre-deployment stage, add a short
decision checkpoint:

- What evidence did this phase produce?
- Did any assumption fail?
- Does the next phase still make sense?
- Does the user need to authorize an external action?

## Final retrospective

End the guide with:

- completed user journey;
- architecture decisions and their consequences;
- known limitations and deferred work;
- operating and recovery instructions;
- concepts the user should now be able to explain;
- a small exercise asking the user to draft a future improvement prompt;
- recommended teaching mode for the next project.
