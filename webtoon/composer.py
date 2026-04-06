"""
Webtoon Video Composer

Converts a folder of webtoon panel images + script into a video.
Supports transitions (fade, slide, zoom), TTS narration, SFX, and BGM.

Input: folder with script.toml + panel PNG files
Output: MP4 video ready for YouTube Shorts or long-form
"""

import os
import tempfile
from pathlib import Path

import toml
from PIL import Image
from moviepy import (
    AudioFileClip,
    ColorClip,
    CompositeAudioClip,
    CompositeVideoClip,
    ImageClip,
    concatenate_videoclips,
)
from moviepy.video.fx import CrossFadeIn, CrossFadeOut, FadeIn, FadeOut
from rich.console import Console

from tts.engine import TTSEngine

console = Console()


class WebtoonComposer:
    """Composes video from webtoon panels + script."""

    def __init__(self, width: int = 1080, height: int = 1920, fps: int = 30):
        self.width = width
        self.height = height
        self.fps = fps
        self.transition_duration = 0.4  # seconds for transitions

    def _fit_panel_to_frame(self, image_path: str) -> str:
        """
        Resize and pad a panel image to fit the video frame.
        Maintains aspect ratio, adds black bars if needed.
        Returns path to the processed image.
        """
        img = Image.open(image_path).convert("RGBA")
        img_w, img_h = img.size

        # Calculate scale to fit within frame
        scale_w = self.width / img_w
        scale_h = self.height / img_h
        scale = min(scale_w, scale_h)

        new_w = int(img_w * scale)
        new_h = int(img_h * scale)
        img = img.resize((new_w, new_h), Image.Resampling.LANCZOS)

        # Create frame with black background
        frame = Image.new("RGB", (self.width, self.height), (15, 15, 15))

        # Center the panel
        x = (self.width - new_w) // 2
        y = (self.height - new_h) // 2
        frame.paste(img, (x, y), img if img.mode == "RGBA" else None)

        # Save to temp file
        temp_path = image_path + "_fitted.jpg"
        frame.save(temp_path, "JPEG", quality=95)
        return temp_path

    def _apply_transition(
        self, clip, effect: str, duration: float
    ):
        """Apply entry/exit transition effects to a clip."""
        t = self.transition_duration

        if effect == "fade":
            clip = clip.with_effects([FadeIn(t), FadeOut(t)])

        elif effect == "slide_left":
            # Slide in from right
            original_pos = clip.pos
            w = self.width

            def slide_pos(t_val):
                if t_val < self.transition_duration:
                    progress = t_val / self.transition_duration
                    return (int(w * (1 - progress)), 0)
                return (0, 0)

            clip = clip.with_position(slide_pos)
            clip = clip.with_effects([FadeOut(t)])

        elif effect == "slide_up":
            h = self.height

            def slide_up_pos(t_val):
                if t_val < self.transition_duration:
                    progress = t_val / self.transition_duration
                    return (0, int(h * (1 - progress)))
                return (0, 0)

            clip = clip.with_position(slide_up_pos)
            clip = clip.with_effects([FadeOut(t)])

        elif effect == "zoom":
            # Zoom in effect
            def zoom_func(t_val):
                if t_val < self.transition_duration:
                    progress = t_val / self.transition_duration
                    return 0.8 + 0.2 * progress  # 80% -> 100%
                if t_val > duration - self.transition_duration:
                    remaining = duration - t_val
                    progress = remaining / self.transition_duration
                    return 1.0 + 0.1 * (1 - progress)  # 100% -> 110%
                return 1.0

            clip = clip.resized(zoom_func)
            clip = clip.with_effects([FadeIn(t * 0.5), FadeOut(t)])

        else:  # "none" or unknown
            pass

        return clip

    def compose(
        self,
        project_dir: str,
        output_path: str | None = None,
        tts_config: dict | None = None,
    ) -> str | None:
        """
        Compose a webtoon video from a project directory.

        Args:
            project_dir: Path to folder with script.toml + panel images
            output_path: Output MP4 path (auto-generated if None)
            tts_config: TTS configuration dict

        Returns:
            Path to output MP4, or None on failure
        """
        project = Path(project_dir)
        script_path = project / "script.toml"

        if not script_path.exists():
            console.print(f"[red]script.toml not found in {project_dir}[/red]")
            return None

        # Load script
        with open(script_path, "r", encoding="utf-8") as f:
            script = toml.load(f)

        meta = script.get("meta", {})
        panels = script.get("panels", [])

        if not panels:
            console.print("[red]No panels defined in script.toml[/red]")
            return None

        title = meta.get("title", project.name)
        language = meta.get("language", "en")
        bgm_path = meta.get("bgm", "")

        console.print(f"[cyan]Composing webtoon: {title}[/cyan]")
        console.print(f"  [dim]{len(panels)} panels[/dim]")

        # Initialize TTS
        if tts_config is None:
            tts_config = {"tts": {"engine": "gtts", "language": language}}
        tts_engine = TTSEngine(tts_config)

        # Generate TTS and build clips
        temp_dir = tempfile.mkdtemp(prefix="webtoon_")
        panel_clips = []
        audio_clips = []
        current_time = 0.0
        fitted_files = []  # Track temp files for cleanup

        for i, panel in enumerate(panels):
            image_file = panel.get("image", "")
            image_path = str(project / image_file)

            if not os.path.exists(image_path):
                console.print(f"  [yellow]Panel not found: {image_file}[/yellow]")
                continue

            tts_text = panel.get("tts", "")
            effect = panel.get("effect", "fade")
            sfx_file = panel.get("sfx", "")
            panel_duration = panel.get("duration", 3.0)

            # Generate TTS audio if text provided
            tts_audio = None
            if tts_text:
                tts_path = os.path.join(temp_dir, f"panel_{i:03d}.mp3")
                result = tts_engine.generate_audio(tts_text, tts_path)
                if result:
                    tts_audio = AudioFileClip(result)
                    # Use TTS duration if longer than specified
                    panel_duration = max(panel_duration, tts_audio.duration + 0.5)

            # Fit panel image to frame
            fitted_path = self._fit_panel_to_frame(image_path)
            fitted_files.append(fitted_path)

            # Create image clip
            img_clip = ImageClip(fitted_path, duration=panel_duration)

            # Apply transition effect
            img_clip = self._apply_transition(img_clip, effect, panel_duration)

            # Position and timing
            img_clip = img_clip.with_start(current_time)
            panel_clips.append(img_clip)

            # Audio: TTS
            if tts_audio:
                audio_clips.append(tts_audio.with_start(current_time + 0.3))

            # Audio: SFX
            if sfx_file:
                sfx_path = str(project / sfx_file)
                if os.path.exists(sfx_path):
                    sfx_audio = AudioFileClip(sfx_path)
                    audio_clips.append(sfx_audio.with_start(current_time))

            console.print(
                f"  [green][{i+1}/{len(panels)}][/green] {image_file} "
                f"({panel_duration:.1f}s, {effect})"
            )

            current_time += panel_duration

        if not panel_clips:
            console.print("[red]No valid panels to compose.[/red]")
            return None

        total_duration = current_time

        try:
            # Background (black)
            bg = ColorClip(
                size=(self.width, self.height),
                color=(15, 15, 15),
                duration=total_duration,
            )

            # Compose video
            final_video = CompositeVideoClip(
                [bg] + panel_clips,
                size=(self.width, self.height),
            )

            # Mix audio
            if audio_clips:
                all_audio = list(audio_clips)

                # Add BGM if specified
                if bgm_path and os.path.exists(str(project / bgm_path)):
                    bgm = AudioFileClip(str(project / bgm_path))
                    if bgm.duration >= total_duration:
                        bgm = bgm.subclipped(0, total_duration)
                    bgm = bgm.with_volume_scaled(0.15)
                    all_audio.append(bgm.with_start(0))

                mixed_audio = CompositeAudioClip(all_audio)
                final_video = final_video.with_audio(mixed_audio)

            final_video = final_video.with_duration(total_duration)

            # Output path
            if output_path is None:
                output_dir = "output/webtoon"
                os.makedirs(output_dir, exist_ok=True)
                safe_title = "".join(
                    c if c.isalnum() or c in " -_" else "" for c in title
                )[:50]
                output_path = os.path.join(output_dir, f"{safe_title}.mp4")

            # Render
            console.print(f"  [dim]Rendering {total_duration:.1f}s video...[/dim]")
            final_video.write_videofile(
                output_path,
                fps=self.fps,
                codec="libx264",
                audio_codec="aac",
                bitrate="8M",
                preset="medium",
                logger=None,
            )

            final_video.close()

            file_size = os.path.getsize(output_path) / (1024 * 1024)
            console.print(
                f"  [green][OK][/green] Saved: {output_path} "
                f"({total_duration:.1f}s, {file_size:.1f}MB)"
            )
            return output_path

        except Exception as e:
            console.print(f"[red]Composition error: {e}[/red]")
            import traceback
            traceback.print_exc()
            return None

        finally:
            # Cleanup temp files
            import shutil
            shutil.rmtree(temp_dir, ignore_errors=True)
            for f in fitted_files:
                if os.path.exists(f):
                    os.remove(f)
