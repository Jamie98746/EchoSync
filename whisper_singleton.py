"""Whisper model singleton manager."""

import threading
import shutil

_wmodel = None
_wlock = threading.Lock()


def _whisper(size="base"):
    """Return a global Whisper model instance (lazy-loaded)."""
    global _wmodel
    with _wlock:
        if _wmodel is None:
            try:
                import whisper
            except ImportError:
                raise RuntimeError("Please install: pip install openai-whisper")

            if shutil.which("ffmpeg") is None:
                raise RuntimeError(
                    "ffmpeg is missing (Whisper requires it for audio decoding).\n"
                    "Please install ffmpeg and ensure it is on your PATH, e.g.:\n"
                    "  winget install ffmpeg\n"
                    "or download from https://ffmpeg.org/download.html and add it to your PATH."
                )

            print(f"[Whisper] loading model {size} …")
            _wmodel = whisper.load_model(size)
            print("[Whisper] ready")
    return _wmodel
