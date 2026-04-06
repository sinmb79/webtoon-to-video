# Webtoon Script Format

Place your webtoon project in a folder with this structure:

```
my-comic/
  script.toml        # Script file (timing, text, effects)
  panel_01.png        # Panel images in order
  panel_02.png
  panel_03.png
  ...
  sfx/                # Optional sound effects
    punch.mp3
    laugh.mp3
```

## script.toml Format

```toml
[meta]
title = "My Comic Episode 1"
author = "YourName"
language = "en"          # TTS language
bgm = ""                 # Optional BGM file path or leave empty

[[panels]]
image = "panel_01.png"
duration = 3.0           # Seconds to show this panel
tts = "Once upon a time, there was a small ghost..."
effect = "fade"          # fade, slide_left, slide_up, zoom, none
sfx = ""                 # Optional sound effect file

[[panels]]
image = "panel_02.png"
duration = 4.0
tts = "He lived in an old house on the hill."
effect = "slide_left"
sfx = ""

[[panels]]
image = "panel_03.png"
duration = 3.5
tts = "But nobody was afraid of him."
effect = "zoom"
sfx = "sfx/laugh.mp3"
```

## Run

```bash
python webtoon_make.py my-comic/
python webtoon_make.py my-comic/ --output my-video.mp4
```
