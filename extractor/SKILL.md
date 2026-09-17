---
name: extractor
description: Analyze a YouTube video from a URL or video ID, extract its public transcript, and connect its ideas to the user's current workflow or practical goals.
---

# YouTube Video Extractor

Use this skill when the user gives a YouTube video and wants to understand it, remember what it teaches, or decide whether its ideas are useful for a current project or day-to-day task.

## Core workflow

1. Parse the supplied YouTube URL or video ID. Accept normal watch URLs, `youtu.be` links, Shorts, embeds, live links, and a bare 11-character video ID.
2. Extract public captions using the fallback sequence below. Do not report failure until every available route has been attempted.
3. Read the returned metadata and cleaned transcript. Treat absent metadata as unavailable rather than guessing.
4. Treat the transcript as evidence. Separate what the speaker said from your own recommendations and inferences.
5. If the transcript remains unavailable, explain the concrete reason and ask the user to provide captions or another accessible transcript. Do not invent the video's contents or claim to have watched visuals that are absent from the transcript.
6. Match the response depth to the request. A summary-only request should stay concise; workflow mapping should be included when requested or clearly useful.

## Extraction fallback sequence

If `agent-reach` or `yt-dlp` is available, try public subtitles first:

```bash
yt-dlp --write-sub --write-auto-sub --sub-lang "en,zh-Hans,zh" --sub-format vtt --skip-download -o "/tmp/%(id)s.%(ext)s" "VIDEO_URL"
```

If that command fails because of an incompatible local configuration option, retry once with `--ignore-config`. If it fails again, produces no subtitle file, or YouTube blocks the request, run the bundled helper:

```bash
uv run --with youtube-transcript-api python scripts/fetch_transcript.py "VIDEO_URL" --format markdown
```

If `uv` is unavailable but the dependency is already installed, use:

```bash
python3 scripts/fetch_transcript.py "VIDEO_URL" --format markdown
```

If Python reports that `youtube-transcript-api` is missing and environment changes are allowed, install it with `python3 -m pip install youtube-transcript-api`. Otherwise report the missing dependency and provide the command instead of silently modifying the environment.

Both extraction routes use public captions and do not require the user's YouTube account, cookies, or login.

## Response format

Use only the sections needed for the request.

### What this video is about

Give a short, accurate overview and identify the intended audience or problem.

### Main ideas

Explain the important concepts in plain language. Preserve technical terms when they matter, but define them briefly.

### Useful for your workflow

Include this section when the user provides a project, workflow, or practical goal. Map relevant ideas to that context and explain:

- what it enables;
- why it may matter now;
- the smallest practical next step.

If nothing is directly relevant, say so clearly and explain what would need to change for it to become useful.

### Action plan

Include this section when the user asks what to do next or when the video is explicitly instructional. Give a short ordered list and distinguish actions supported by the video from recommendations made by the agent.

### Caveats

Call out claims that depend on version, pricing, access, permissions, or a specific vendor. Flag missing context, uncertain transcript sections, and advice that should be verified before use.

## Handling long videos

Do not summarize every sentence. Organize the transcript into concepts, workflows, examples, and claims. Prefer paraphrase and do not reproduce the complete transcript. If timestamps are available, include them for especially useful sections.

## Boundaries

- This skill extracts captions/transcripts; it does not prove that the agent has seen visual demonstrations, slides, code, or on-screen UI that is absent from the transcript.
- Do not use private account data or bypass access controls.
- Do not treat the speaker's opinion as verified fact. Identify claims that need independent checking.
- Keep the user's current workflow as the organizing principle rather than producing a generic video summary.
- The bundled helper returns JSON with cleaned timestamped segments and best-effort metadata. Its Markdown output groups the transcript into timestamped sections. Use `--language en --language hi` to provide language preferences.
