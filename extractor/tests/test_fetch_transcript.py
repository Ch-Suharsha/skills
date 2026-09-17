from __future__ import annotations

import sys
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path


SCRIPT_PATH = Path(__file__).parents[1] / "scripts" / "fetch_transcript.py"
SPEC = spec_from_file_location("youtube_video_analyst_fetch_transcript", SCRIPT_PATH)
assert SPEC and SPEC.loader
MODULE = module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


def test_extract_video_id_supports_common_youtube_inputs() -> None:
    video_id = "Fruw822BMBc"
    inputs = [
        video_id,
        f"https://youtu.be/{video_id}?si=example",
        f"https://www.youtube.com/watch?v={video_id}&t=10",
        f"https://www.youtube.com/shorts/{video_id}",
        f"https://www.youtube.com/embed/{video_id}",
        f"https://www.youtube.com/live/{video_id}",
    ]
    assert [MODULE.extract_video_id(value) for value in inputs] == [video_id] * 6


def test_clean_segments_removes_noise_and_consecutive_duplicates() -> None:
    segments = [
        MODULE.Segment(0, 1, "[Music]"),
        MODULE.Segment(1, 1, "  Hello   &amp; welcome  "),
        MODULE.Segment(2, 1, "hello & welcome"),
        MODULE.Segment(3, 1, "[Applause] Next idea"),
    ]
    assert MODULE.clean_segments(segments) == [
        MODULE.Segment(1, 1, "Hello & welcome"),
        MODULE.Segment(3, 1, "Next idea"),
    ]


def test_render_markdown_contains_metadata_and_timestamped_sections() -> None:
    metadata = MODULE.VideoMetadata(
        title="Example video",
        channel="Example channel",
        channel_url="https://www.youtube.com/@example",
        published_at="2026-09-17",
        duration_seconds=125,
    )
    segments = [
        MODULE.Segment(5, 2, "First idea."),
        MODULE.Segment(70, 2, "Second idea."),
    ]
    output = MODULE.render_markdown(
        "Fruw822BMBc", segments, "en", metadata, window_seconds=60
    )
    assert "# Example video" in output
    assert "**Channel:** [Example channel]" in output
    assert "**Published:** 2026-09-17" in output
    assert "### [00:00–01:00]" in output
    assert "### [01:00–02:00]" in output
    assert "First idea." in output
    assert "Second idea." in output
