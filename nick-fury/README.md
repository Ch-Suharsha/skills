# Nick Fury

Nick Fury is a project-planning and teaching skill for people who have a product
idea but do not yet know how to direct a coding agent like a senior engineer.

You explain the idea once—through chat, requirement files, an existing
repository, or a combination of them. Nick Fury clarifies the decisions that
matter and generates a project-specific sequence of prompts that you can copy
into Codex, Claude Code, Hermes, or another coding agent.

## What problem it solves

Broad prompts such as "build my application" leave many architectural and
product decisions unstated. Writing a complete engineering prompt for every
stage is also overwhelming for a newer developer.

Nick Fury sits between those two extremes. It creates the detailed prompts for
you while explaining:

- why each prompt appears at that stage;
- how it gives the coding agent useful direction;
- what trade-offs the step introduces;
- what result should be produced;
- how to verify the result before continuing;
- what engineering concept you are learning.

## Two ways to begin

### Start from requirement files

Point the agent to the available Markdown, text, PDF, diagrams, or repository and
ask it to use Nick Fury:

```text
Use $nick-fury. Read the requirement documents I provided, summarize what you
understand, and ask only the questions that would materially change the project.
After we clarify them, create my project brief and guided build plan.
```

### Start from a conversation

Describe the project naturally:

```text
Use $nick-fury. I want to build an application that [describe the idea in your
own words]. Help me clarify it and then create a guided sequence of copy-paste
prompts for my coding agent.
```

You do not need to know the final architecture or write formal requirements.

## What it creates

Inside an existing project, Nick Fury produces:

```text
docs/
├── project-brief.md
└── project-build-guide.md
```

`project-brief.md` records stable context such as users, goals, requirements,
technology decisions, assumptions, and the first useful release.

`project-build-guide.md` contains:

- a product summary and Mermaid mind map;
- a dependency-aware roadmap;
- a dynamic number of copy-paste prompts;
- explanations and trade-offs under every prompt;
- progress and verification checkboxes;
- learning checkpoints and a final retrospective.

The number of prompts is based on project complexity. It is not fixed.

## How the prompts stay token-efficient

The detailed project context is written once in `project-brief.md`. Later prompts
tell the coding agent to read that file and inspect the current repository,
instead of repeating the full idea every time. Each prompt still includes a
clear objective, requirements, constraints, acceptance criteria, and
verification instructions.

## How it teaches you

Nick Fury defaults to a guided beginner mode. It explains unfamiliar commands
and architecture decisions when they first appear. Later phases use shorter
reminders and ask you to predict decisions or draft part of a prompt yourself.

The long-term goal is for you to need less guidance after completing several
projects—not to depend on the skill permanently.

## Safety defaults

Generated prompts normally instruct the coding agent to:

- inspect an existing repository before changing it;
- preserve unrelated work;
- keep secrets out of source control;
- test meaningful changes;
- ask before committing, pushing, deploying, sending messages, making purchases,
  or deleting data unless that action was explicitly authorized.

## Install for Codex

Clone the repository and copy the skill into the Codex skills directory:

```bash
git clone https://github.com/Ch-Suharsha/skills.git
cp -R skills/nick-fury ~/.codex/skills/nick-fury
```

Restart or refresh the agent session if needed, then invoke it with
`$nick-fury`.

## Portability

The core instructions are agent-neutral. Systems that support `SKILL.md` can use
the folder directly. For other coding agents, provide `SKILL.md` as project or
agent instructions and keep the `references/` directory accessible.

Capabilities still depend on the host agent. For example, the agent must have an
appropriate document-reading tool to understand a PDF reliably.
