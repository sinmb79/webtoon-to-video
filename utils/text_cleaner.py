"""Text cleaning utilities for Reddit content."""

import re
import textwrap


def wrap_text(text: str, max_width: int = 35) -> str:
    """Wrap text to fit within a given character width for subtitle display."""
    return "\n".join(textwrap.wrap(text, width=max_width))


def truncate_text(text: str, max_length: int = 200) -> str:
    """Truncate text to a maximum length, breaking at word boundary."""
    if len(text) <= max_length:
        return text
    return text[:max_length].rsplit(" ", 1)[0] + "..."


def format_score(score: int) -> str:
    """Format score for display (e.g., 1.2k, 15.3k)."""
    if score >= 1000:
        return f"{score / 1000:.1f}k"
    return str(score)


def sanitize_filename(text: str) -> str:
    """Create a safe filename from text."""
    # Remove special characters
    safe = re.sub(r'[<>:"/\\|?*]', "", text)
    # Replace spaces with underscores
    safe = re.sub(r"\s+", "_", safe)
    # Limit length
    return safe[:80]
