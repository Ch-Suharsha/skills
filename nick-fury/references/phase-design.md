# Phase design

Use this reference when converting a clarified project brief into an ordered
roadmap. Select phases because the project needs them, not because this document
mentions them.

## Design from risk and dependency

Order work using these questions:

1. What assumption could invalidate the product or architecture?
2. What is the smallest user journey that proves useful value?
3. Which foundations are required before that journey can run?
4. Which integrations are uncertain enough to test early?
5. What can safely wait until the vertical slice works?

Do not begin by building every foundation in isolation. Create only enough
foundation to support a thin end-to-end slice, then harden and expand it.

## Candidate phases

Choose and combine candidates according to complexity:

### Product clarification

Use when requirements, users, success criteria, or scope remain unclear. The
deliverable is an approved project brief, not code.

### Existing-system audit

Use for a non-empty repository. Inspect architecture, dependencies, packaging,
tests, Git status, and constraints before proposing changes.

### Technical decisions

Use when the stack or architecture has meaningful alternatives. Record only
decisions that affect implementation. Avoid lengthy comparisons for reversible,
low-impact choices.

### Project foundation

Establish packaging, configuration, secrets handling, basic quality tools, and
the smallest useful folder structure. Include exact initialization commands only
after selecting the stack.

### Vertical slice

Implement one realistic input-to-output journey across the necessary layers.
Use real external integration only when safe and useful; otherwise combine
fixtures with one explicit integration check.

### Persistence and migrations

Use when durable state is required. Define ownership, constraints, duplicate
behavior, transaction boundaries, and schema migration from the beginning.

### External integrations

Give each unstable boundary an adapter, timeout, error behavior, and fixture-
based tests. Test authentication or rate limits early when they are a major risk.

### AI behavior

Separate deterministic application logic from model judgment. Define structured
outputs, grounding, failure behavior, cost controls, and a small evaluation set.

### User experience

Build the smallest interface needed for the validated workflow. Include empty,
loading, error, and permission states when applicable.

### Reliability and security

Add retries, idempotency, observability, access controls, secret handling,
backups, and failure recovery in proportion to actual risk.

### Integration and regression

Join independently tested parts, exercise realistic paths, and verify repeated
execution. Include a failure review before deployment.

### Deployment and operations

Package the application, configure environments, migrate the production
database, deploy, schedule jobs, and verify logs or health checks. Separate
reversible preparation from consequential external changes.

### Documentation and release

Document setup, architecture, commands, limitations, and operation. Audit
secrets and repository history before public release.

## Phase sizing

One prompt should produce one coherent, verifiable outcome. Split a phase when:

- it contains independent external side effects;
- failure would obscure which component is responsible;
- it mixes architecture approval with implementation;
- its verification requires several unrelated systems;
- the coding agent would need to make multiple unapproved product decisions.

Combine work when the pieces are small, tightly coupled, and verified together.

## Dependency rules

- Clarify behavior before choosing irreversible architecture.
- Establish package execution before adding many modules.
- Add schema migrations before production data matters.
- Verify one integration before generalizing an adapter system.
- Validate structured model output before building downstream consumers.
- Render messages or payments in dry-run mode before real delivery or charges.
- Make the local path work before containerizing it.
- Test the container before deploying it.
- Verify staging or dry-run behavior before scheduling production automation.
- Audit secrets before making a repository public.

## Keep the roadmap adaptive

Mark optional phases and the condition that activates them. After each major
milestone, include a checkpoint asking whether evidence changed the scope,
architecture, or next phase. Update downstream prompts rather than preserving a
plan known to be wrong.
