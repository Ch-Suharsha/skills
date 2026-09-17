# Skills

Reusable AI-agent skills maintained by Harsha.

## Available skills

### Extractor

`extractor` accepts a YouTube URL or video ID, retrieves its public transcript,
cleans and timestamps it, collects basic video metadata, and helps relate the
video's ideas to a practical workflow.

The skill does not require a YouTube account, cookies, or private account data.
It can only process videos with publicly accessible captions.

## Repository structure

```text
skills/
└── extractor/
    ├── SKILL.md
    ├── agents/
    ├── scripts/
    └── tests/
```

Future skills should be added as additional top-level directories alongside
`extractor`.

## Install

Clone the repository and copy the desired skill into your agent's skills
directory. For Codex:

```bash
git clone https://github.com/Ch-Suharsha/skills.git
cp -R skills/extractor ~/.codex/skills/extractor
```

Then invoke it with a prompt such as:

```text
Use $extractor with this YouTube URL and explain which ideas are useful for my current workflow.
```

The bundled transcript helper can also be run directly:

```bash
uv run --with youtube-transcript-api python extractor/scripts/fetch_transcript.py "YOUTUBE_URL" --format markdown
```

## Test

```bash
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 uv run --with pytest pytest -q extractor/tests
```
