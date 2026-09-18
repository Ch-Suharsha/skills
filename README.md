# Skills

A collection of reusable AI-agent skills.

## Available skills

| Skill | Purpose | Documentation |
| --- | --- | --- |
| `extractor` | Extract and analyze public YouTube transcripts for practical workflow insights. | [Read the extractor guide](extractor/README.md) |
| `nick-fury` | Turn a project idea into an adaptive, educational sequence of coding-agent prompts. | [Read the Nick Fury guide](nick-fury/README.md) |

## Repository structure

```text
skills/
├── extractor/
│   ├── README.md
│   ├── SKILL.md
│   ├── agents/
│   ├── scripts/
│   └── tests/
└── nick-fury/
    ├── README.md
    ├── SKILL.md
    ├── agents/
    └── references/
```

Future skills should be added as additional top-level directories. Every skill
directory should contain its own README so people can
understand its purpose and usage without reading its internal agent instructions.

## Install

Clone the repository and copy the desired skill into your agent's skills
directory. For Codex:

```bash
git clone https://github.com/Ch-Suharsha/skills.git
cp -R skills/extractor ~/.codex/skills/extractor
# Or install Nick Fury:
cp -R skills/nick-fury ~/.codex/skills/nick-fury
```

Then invoke it with a prompt such as:

```text
Use $extractor with this YouTube URL and explain which ideas are useful for my current workflow.

Use $nick-fury to turn my project idea into a guided, copy-paste build plan.
```

The bundled transcript helper can also be run directly:

```bash
uv run --with youtube-transcript-api python extractor/scripts/fetch_transcript.py "YOUTUBE_URL" --format markdown
```

## Test

```bash
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 uv run --with pytest pytest -q extractor/tests
```
