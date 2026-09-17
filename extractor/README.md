# YouTube Video Extractor

`extractor` is a reusable AI-agent skill for understanding YouTube videos from
their publicly available captions. Give an agent a YouTube URL or video ID and
the skill helps it extract the transcript, identify the main ideas, and connect
those ideas to a project or workflow.

## What it is useful for

- Summarizing educational or technical YouTube videos.
- Identifying the video's most important ideas and recommendations.
- Finding which parts are relevant to a current project or workflow.
- Turning an instructional video into a practical action plan.
- Producing a cleaned, timestamped transcript in Markdown or JSON.

## What the skill extracts

- Video title and ID.
- Channel name and channel URL.
- Publication date and duration when available.
- Public captions with common noise markers and repeated lines removed.
- Timestamped transcript sections for easier navigation.

## Supported inputs

- Standard YouTube watch URLs.
- `youtu.be` sharing links.
- YouTube Shorts URLs.
- Embed and live-video URLs.
- A bare 11-character YouTube video ID.

## Requirements

- Python 3.10 or newer.
- [`uv`](https://docs.astral.sh/uv/) is recommended for portable execution.
- The video must have publicly accessible captions or automatic captions.

No YouTube account, cookies, API key, or private account information is needed.

## Install for Codex

Clone this repository and copy the skill into the Codex skills directory:

```bash
git clone https://github.com/Ch-Suharsha/skills.git
cp -R skills/extractor ~/.codex/skills/extractor
```

Restart or refresh your agent session if needed so it can discover the new
skill.

## Use with an agent

Invoke the skill by name and provide both the video and the context you care
about:

```text
Use $extractor with https://youtu.be/VIDEO_ID. Summarize the video and explain
which ideas could improve my current AI development workflow.
```

For a shorter result:

```text
Use $extractor with this YouTube link and give me only the five main ideas.
```

The response adapts to the request. It can provide a concise summary, workflow
mapping, action plan, or caveats without always producing every section.

## Run the transcript helper directly

From the repository root, generate timestamped Markdown:

```bash
uv run --with youtube-transcript-api python extractor/scripts/fetch_transcript.py \
  "YOUTUBE_URL" --format markdown
```

Generate structured JSON:

```bash
uv run --with youtube-transcript-api python extractor/scripts/fetch_transcript.py \
  "YOUTUBE_URL" --format json
```

Provide preferred transcript languages by repeating `--language`:

```bash
uv run --with youtube-transcript-api python extractor/scripts/fetch_transcript.py \
  "YOUTUBE_URL" --language en --language hi --format markdown
```

## How extraction works

The skill first tries an available subtitle extraction tool such as `yt-dlp`.
If local configuration causes a failure, it retries without that configuration.
It then falls back to the bundled Python helper powered by
`youtube-transcript-api`.

All routes use public captions. The skill does not bypass private videos,
members-only content, regional restrictions, or other access controls.

## Limitations

- Videos without accessible captions cannot be transcribed by this skill.
- Captions may contain recognition errors, especially for names or technical terms.
- Transcript analysis cannot reliably describe visuals, slides, demonstrations,
  or code that the speaker does not explain aloud.
- Video claims should be independently verified when accuracy is important.

## Test

```bash
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 uv run --with pytest pytest -q extractor/tests
```

The tests cover common YouTube URL formats, transcript cleanup, metadata
rendering, and timestamped Markdown output.
