# Webtoon to Video

직접 그린 웹툰 이미지를 YouTube 영상으로 변환해주는 도구입니다.

패널 이미지(PNG)와 간단한 스크립트 파일만 있으면, TTS 음성 + 전환 효과 + 배경 음악이 포함된 영상을 자동으로 만들어줍니다.

> [English version (README_EN.md)](./README_EN.md)

---

## 어떤 프로그램인가요?

웹툰 패널 이미지들을 순서대로 보여주면서, 각 장면에 맞는 음성과 효과를 자동으로 입혀 영상으로 만들어줍니다.

```
웹툰 패널 PNG + script.toml → TTS 음성 + 전환 효과 + BGM → MP4 영상
```

## 주요 기능

- 패널 이미지(PNG/JPG)를 순서대로 영상으로 합성
- 패널별 TTS 음성 자동 생성 (한국어/영어 등)
- 전환 효과: fade, slide_left, slide_up, zoom
- 효과음(SFX) 지원
- 배경 음악(BGM) 믹싱
- 세로(1080x1920 Shorts) / 가로(1920x1080) 모두 지원
- 샘플 프로젝트 포함

## 설치

```bash
git clone https://github.com/sinmb79/webtoon-to-video.git
cd webtoon-to-video
pip install -r requirements.txt
```

## 사용법

### 기본 실행

```bash
python webtoon_make.py my-comic/
```

### 옵션

```bash
# 출력 파일 지정
python webtoon_make.py my-comic/ --output my-video.mp4

# 한국어 TTS
python webtoon_make.py my-comic/ --lang ko

# 가로 영상 (일반 YouTube용)
python webtoon_make.py my-comic/ --width 1920 --height 1080
```

### 샘플 실행

```bash
python webtoon_make.py webtoon/samples/ghost-story/
```

## 프로젝트 폴더 만들기

웹툰 프로젝트는 이렇게 구성합니다:

```
my-comic/
  script.toml        # 스크립트 (대사, 효과, 타이밍)
  panel_01.png        # 패널 이미지 (직접 그린 것)
  panel_02.png
  panel_03.png
  sfx/                # 효과음 (선택사항)
    laugh.mp3
```

### script.toml 작성법

```toml
[meta]
title = "내 웹툰 에피소드 1"
author = "작가이름"
language = "ko"
bgm = ""              # BGM 파일 경로 (선택)

[[panels]]
image = "panel_01.png"
duration = 4.0         # 이 패널을 보여줄 시간 (초)
tts = "옛날 옛적에 작은 유령이 살았습니다."
effect = "fade"        # 전환 효과

[[panels]]
image = "panel_02.png"
duration = 3.5
tts = "매일 밤 사람들을 놀라게 하려고 했죠."
effect = "slide_left"

[[panels]]
image = "panel_03.png"
duration = 4.0
tts = "하지만 모두가 귀엽다고만 했습니다."
effect = "zoom"
sfx = "sfx/laugh.mp3"  # 효과음 추가
```

### 전환 효과 종류

| 효과 | 설명 |
|------|------|
| `fade` | 페이드 인/아웃 |
| `slide_left` | 오른쪽에서 슬라이드 |
| `slide_up` | 아래에서 슬라이드 |
| `zoom` | 줌 인 효과 |
| `none` | 전환 효과 없음 |

## 프로젝트 구조

```
webtoon-to-video/
├── webtoon_make.py         # 실행 파일
├── webtoon/
│   ├── composer.py         # 영상 합성 엔진
│   ├── script_format.md    # 스크립트 작성 가이드
│   └── samples/            # 샘플 프로젝트
│       └── ghost-story/    # "The Friendliest Ghost"
├── tts/engine.py           # TTS 음성 생성
├── utils/                  # 유틸리티
└── requirements.txt        # 의존성
```

## 라이선스

MIT License
