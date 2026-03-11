"""Detect what features are available in the current environment (local/cloud)."""

import os
import shutil


def _has(pkg: str) -> bool:
    """Check whether a given Python package is installed."""
    import importlib

    try:
        importlib.import_module(pkg)
        return True
    except ImportError:
        return False


def get_capabilities() -> dict:
    return {
        "local_stt": _has("whisper"),
        "local_tts": _has("edge_tts"),
        "local_ffmpeg": shutil.which("ffmpeg") is not None,
        "cloud_ready": bool(os.environ.get("OPENAI_API_KEY")),
    }
