#!/usr/bin/env python3
"""Fetch and clean a public YouTube transcript with best-effort metadata."""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
from dataclasses import asdict, dataclass
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import parse_qs, urlencode, urlparse
from urllib.request import Request, urlopen


VIDEO_ID_PATTERN = re.compile(r"^[A-Za-z0-9_-]{11}$")
WHITESPACE_PATTERN = re.compile(r"\s+")
NOISE_PATTERN = re.compile(
    r"\[(?:music|applause|laughter|inaudible|silence|foreign)\]",
    flags=re.IGNORECASE,
)
PUBLISHED_PATTERNS = (
    re.compile(r'"publishDate"\s*:\s*"([^"]+)"'),
    re.compile(r'"uploadDate"\s*:\s*"([^"]+)"'),
    re.compile(r'<meta\s+itemprop="datePublished"\s+content="([^"]+)"'),
)
DURATION_PATTERN = re.compile(r'"lengthSeconds"\s*:\s*"?(\d+)"?')
USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"
)


@dataclass(frozen=True)
class Segment:
    start: float
    duration: float
    text: str


@dataclass(frozen=True)
class VideoMetadata:
    title: str | None = None
    channel: str | None = None
    channel_url: str | None = None
    published_at: str | None = None
    duration_seconds: float | None = None
    thumbnail_url: str | None = None


def extract_video_id(value: str) -> str:
    """Extract and validate a YouTube video ID from a URL or bare ID."""
    candidate = value.strip()
    if VIDEO_ID_PATTERN.fullmatch(candidate):
        return candidate

    parsed = urlparse(candidate)
    if parsed.scheme not in {"http", "https"} or parsed.netloc.lower() not in {
        "youtube.com",
        "www.youtube.com",
        "m.youtube.com",
        "youtu.be",
        "www.youtu.be",
    }:
        raise ValueError("Expected a YouTube URL or an 11-character YouTube video ID")

    host = parsed.netloc.lower()
    if host.endswith("youtu.be"):
        candidate = parsed.path.strip("/").split("/", 1)[0]
    elif parsed.path == "/watch":
        candidate = parse_qs(parsed.query).get("v", [""])[0]
    else:
        parts = [part for part in parsed.path.split("/") if part]
        if parts and parts[0] in {"shorts", "embed", "live"}:
            candidate = parts[1] if len(parts) > 1 else ""
        else:
            candidate = ""

    if not VIDEO_ID_PATTERN.fullmatch(candidate):
        raise ValueError(f"Could not find a valid YouTube video ID in: {value}")
    return candidate


def _number(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def clean_caption_text(value: str) -> str:
    """Normalize caption text and remove common non-speech markers."""
    text = html.unescape(value)
    text = NOISE_PATTERN.sub(" ", text)
    return WHITESPACE_PATTERN.sub(" ", text).strip()


def clean_segments(segments: list[Segment]) -> list[Segment]:
    """Remove empty/noise-only and consecutive duplicate transcript segments."""
    cleaned: list[Segment] = []
    previous_text: str | None = None
    for segment in segments:
        text = clean_caption_text(segment.text)
        normalized = text.casefold()
        if not text or normalized == previous_text:
            continue
        cleaned.append(Segment(start=segment.start, duration=segment.duration, text=text))
        previous_text = normalized
    return cleaned


def _fetch(video_id: str, languages: list[str]) -> tuple[list[Segment], str | None]:
    try:
        from youtube_transcript_api import YouTubeTranscriptApi
    except ImportError as exc:
        raise RuntimeError(
            "youtube-transcript-api is not installed. Run with: "
            "uv run --with youtube-transcript-api python scripts/fetch_transcript.py VIDEO"
        ) from exc

    transcript = YouTubeTranscriptApi().fetch(video_id, languages=languages or ["en"])
    segments: list[Segment] = []
    for snippet in transcript:
        if hasattr(snippet, "text"):
            text = str(snippet.text)
            start = _number(getattr(snippet, "start", 0.0))
            duration = _number(getattr(snippet, "duration", 0.0))
        else:
            text = str(snippet.get("text", ""))
            start = _number(snippet.get("start"))
            duration = _number(snippet.get("duration"))
        segments.append(Segment(start=start, duration=duration, text=text))

    language_code = getattr(transcript, "language_code", None)
    return clean_segments(segments), language_code


def _request_text(url: str, *, timeout: float = 15.0) -> str:
    request = Request(url, headers={"User-Agent": USER_AGENT})
    with urlopen(request, timeout=timeout) as response:  # noqa: S310 - fixed HTTPS hosts
        return response.read().decode("utf-8", errors="replace")


def _fetch_oembed_metadata(video_id: str) -> dict[str, Any]:
    query = urlencode(
        {"url": f"https://www.youtube.com/watch?v={video_id}", "format": "json"}
    )
    try:
        payload = json.loads(_request_text(f"https://www.youtube.com/oembed?{query}"))
    except (HTTPError, URLError, TimeoutError, OSError, json.JSONDecodeError):
        return {}
    return {
        "title": payload.get("title"),
        "channel": payload.get("author_name"),
        "channel_url": payload.get("author_url"),
        "thumbnail_url": payload.get("thumbnail_url"),
    }


def _fetch_watch_metadata(video_id: str) -> dict[str, Any]:
    try:
        page = _request_text(f"https://www.youtube.com/watch?v={video_id}")
    except (HTTPError, URLError, TimeoutError, OSError):
        return {}

    published_at = None
    for pattern in PUBLISHED_PATTERNS:
        match = pattern.search(page)
        if match:
            published_at = match.group(1)
            break
    duration_match = DURATION_PATTERN.search(page)
    return {
        "published_at": published_at,
        "duration_seconds": float(duration_match.group(1)) if duration_match else None,
    }


def fetch_metadata(video_id: str, segments: list[Segment]) -> VideoMetadata:
    """Fetch public metadata without making transcript extraction depend on it."""
    metadata = {**_fetch_oembed_metadata(video_id), **_fetch_watch_metadata(video_id)}
    if metadata.get("duration_seconds") is None and segments:
        metadata["duration_seconds"] = max(
            segment.start + segment.duration for segment in segments
        )
    return VideoMetadata(**metadata)


def format_timestamp(seconds: float) -> str:
    total = max(0, int(seconds))
    hours, remainder = divmod(total, 3600)
    minutes, seconds = divmod(remainder, 60)
    if hours:
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    return f"{minutes:02d}:{seconds:02d}"


def group_segments(
    segments: list[Segment], *, window_seconds: int = 60
) -> list[tuple[int, list[Segment]]]:
    groups: dict[int, list[Segment]] = {}
    for segment in segments:
        group_start = int(segment.start // window_seconds) * window_seconds
        groups.setdefault(group_start, []).append(segment)
    return sorted(groups.items())


def render_markdown(
    video_id: str,
    segments: list[Segment],
    language_code: str | None,
    metadata: VideoMetadata | None = None,
    *,
    window_seconds: int = 60,
) -> str:
    """Render metadata and transcript as readable, timestamped Markdown."""
    metadata = metadata or VideoMetadata()
    lines = [f"# {metadata.title or f'YouTube transcript: `{video_id}`'}", ""]
    lines.append(f"- **URL:** https://www.youtube.com/watch?v={video_id}")
    if metadata.channel:
        channel = (
            f"[{metadata.channel}]({metadata.channel_url})"
            if metadata.channel_url
            else metadata.channel
        )
        lines.append(f"- **Channel:** {channel}")
    if metadata.published_at:
        lines.append(f"- **Published:** {metadata.published_at}")
    if metadata.duration_seconds is not None:
        lines.append(f"- **Duration:** {format_timestamp(metadata.duration_seconds)}")
    if language_code:
        lines.append(f"- **Transcript language:** `{language_code}`")

    lines.extend(["", "## Transcript", ""])
    total_seconds = int(metadata.duration_seconds) if metadata.duration_seconds else None
    for start, group in group_segments(segments, window_seconds=window_seconds):
        end = start + window_seconds
        if total_seconds is not None:
            end = min(end, max(start, total_seconds))
        lines.extend(
            [
                f"### [{format_timestamp(start)}–{format_timestamp(end)}]",
                "",
                " ".join(segment.text for segment in group),
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("video", help="YouTube URL or 11-character video ID")
    parser.add_argument(
        "--language",
        action="append",
        dest="languages",
        default=[],
        help="Preferred transcript language; repeat for fallbacks (default: en)",
    )
    parser.add_argument(
        "--format",
        choices=("json", "markdown"),
        default="json",
        help="Output format (default: json)",
    )
    parser.add_argument(
        "--window-seconds",
        type=int,
        default=60,
        help="Seconds per timestamped Markdown section (default: 60)",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    if args.window_seconds < 1:
        print("--window-seconds must be at least 1", file=sys.stderr)
        return 2

    try:
        video_id = extract_video_id(args.video)
        segments, language_code = _fetch(video_id, args.languages)
        metadata = fetch_metadata(video_id, segments)
    except Exception as exc:  # noqa: BLE001 - CLI should explain extraction failures
        print(
            f"Transcript extraction failed ({type(exc).__name__}): {exc}",
            file=sys.stderr,
        )
        return 1

    if args.format == "markdown":
        print(
            render_markdown(
                video_id,
                segments,
                language_code,
                metadata,
                window_seconds=args.window_seconds,
            ),
            end="",
        )
        return 0

    payload = {
        "video_id": video_id,
        "url": f"https://www.youtube.com/watch?v={video_id}",
        **asdict(metadata),
        "language_code": language_code,
        "transcript": "\n".join(segment.text for segment in segments),
        "segments": [asdict(segment) for segment in segments],
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
