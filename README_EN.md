# Webtoon to Video

Convert your webtoon panel images into YouTube-ready videos automatically.

Just provide panel images (PNG) and a simple script file — the tool generates TTS narration, transition effects, and background music.

> [한국어 버전 (README.md)](./README.md)

---

## What is this?

This tool takes webtoon/comic panels and turns them into animated videos with narration, transitions, and sound effects.

```
Panel PNGs + script.toml → TTS + transitions + BGM → MP4 video
```

## Features

- Panel-by-panel animation from PNG/JPG images
- Auto TTS narration per panel (100+ languages via Google TTS)
- Transition effects: fade, slide_left, slide_up, zoom
- Sound effects (SFX) support
- Background music (BGM) mixing
- Vertical (1080x1920 Shorts) and landscape (1920x1080) output
- Sample project included

## Installation

```bash
git clone https://github.com/sinmb79/webtoon-to-video.git
cd webtoon-to-video
pip install -r requirements.txt
```

## Quick Start

```bash
# Run with sample project
python webtoon_make.py webtoon/samples/ghost-story/

# Your own project
python webtoon_make.py my-comic/

# Options
python webtoon_make.py my-comic/ --output video.mp4 --lang ko
python webtoon_make.py my-comic/ --width 1920 --height 1080  # Landscape
```

## Project Folder Structure

```
my-comic/
  script.toml        # Script (dialogue, effects, timing)
  panel_01.png        # Panel images
  panel_02.png
  panel_03.png
  sfx/                # Sound effects (optional)
    laugh.mp3
```

### script.toml Format

```toml
[meta]
title = "My Comic Episode 1"
author = "YourName"
language = "en"
bgm = ""

[[panels]]
image = "panel_01.png"
duration = 4.0
tts = "Once upon a time, there was a small ghost."
effect = "fade"        # fade, slide_left, slide_up, zoom, none
sfx = ""               # Optional sound effect
```

## Transition Effects

| Effect | Description |
|--------|-------------|
| `fade` | Fade in/out |
| `slide_left` | Slide in from right |
| `slide_up` | Slide up from bottom |
| `zoom` | Zoom in effect |
| `none` | No transition |

## License

MIT License
