#!/usr/bin/env python3
"""
Webtoon Video Maker

Converts webtoon panel images + script into YouTube-ready videos.

Usage:
    python webtoon_make.py my-comic/
    python webtoon_make.py my-comic/ --output my-video.mp4
    python webtoon_make.py my-comic/ --width 1080 --height 1920   # Shorts (vertical)
    python webtoon_make.py my-comic/ --width 1920 --height 1080   # Landscape
"""

import argparse
import os
import sys

from rich.console import Console

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from webtoon.composer import WebtoonComposer

console = Console()

BANNER = """
[bold magenta]
 __        __   _     _                    __  __       _
 \\ \\      / /__| |__ | |_ ___   ___  _ __ |  \\/  | __ _| | _____
  \\ \\ /\\ / / _ \\ '_ \\| __/ _ \\ / _ \\| '_ \\| |\\/| |/ _` | |/ / _ \\
   \\ V  V /  __/ |_) | || (_) | (_) | | | | |  | | (_| |   <  __/
    \\_/\\_/ \\___|_.__/ \\__\\___/ \\___/|_| |_|_|  |_|\\__,_|_|\\_\\___|
[/bold magenta]
[dim]Original Webtoon to Video Converter[/dim]
"""


def main():
    console.print(BANNER)

    parser = argparse.ArgumentParser(description="Webtoon Video Maker")
    parser.add_argument("project", type=str, help="Path to webtoon project folder")
    parser.add_argument("--output", "-o", type=str, help="Output MP4 file path")
    parser.add_argument("--width", type=int, default=1080, help="Video width (default: 1080)")
    parser.add_argument("--height", type=int, default=1920, help="Video height (default: 1920)")
    parser.add_argument("--fps", type=int, default=30, help="Frame rate (default: 30)")
    parser.add_argument("--lang", type=str, default="en", help="TTS language (default: en)")
    args = parser.parse_args()

    if not os.path.isdir(args.project):
        console.print(f"[red]Project folder not found: {args.project}[/red]")
        sys.exit(1)

    composer = WebtoonComposer(
        width=args.width,
        height=args.height,
        fps=args.fps,
    )

    tts_config = {"tts": {"engine": "gtts", "language": args.lang}}

    result = composer.compose(
        project_dir=args.project,
        output_path=args.output,
        tts_config=tts_config,
    )

    if result:
        console.print(f"\n[bold green]Done![/bold green] Video saved to: {result}")
    else:
        console.print("\n[red]Failed to create video.[/red]")
        sys.exit(1)


if __name__ == "__main__":
    main()
