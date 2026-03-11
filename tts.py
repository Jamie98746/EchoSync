"""Text-to-Speech (TTS) related functionality."""

import asyncio
import base64
import os
import tempfile

from openai_client import _openai
from utils import estimate_ts, words_to_segs


def tts_cloud(text: str, voice: str, speed: float, model: str, precise: bool):
    c = _openai()
    resp = c.audio.speech.create(model=model, voice=voice, input=text, speed=speed, response_format="mp3")
    audio = resp.content

    if precise:
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp:
            tmp.write(audio)
            path = tmp.name
        try:
            with open(path, "rb") as f:
                tr = c.audio.transcriptions.create(
                    model="whisper-1",
                    file=f,
                    response_format="verbose_json",
                    timestamp_granularities=["word", "segment"],
                )
        finally:
            os.unlink(path)

        words = [
            {"word": w.word, "start": round(w.start, 3), "end": round(w.end, 3)}
            for w in (tr.words or [])
        ]
        segs = []
        for s in (tr.segments or []):
            sw = [
                {"word": w.word, "start": round(w.start, 3), "end": round(w.end, 3)}
                for w in (s.words or [])
            ]
            segs.append({
                "text": s.text.strip(),
                "start": round(s.start, 3),
                "end": round(s.end, 3),
                "words": sw,
            })
        dur = getattr(tr, "duration", None)
    else:
        est = estimate_ts(text, speed)
        words, segs, dur = est["words"], est["segments"], est["duration"]

    return {
        "audio_base64": base64.b64encode(audio).decode(),
        "audio_format": "mp3",
        "words": words,
        "segments": segs,
        "duration": dur,
    }


def tts_local(text: str, voice: str, rate: str, precise: bool):
    try:
        import edge_tts
    except ImportError:
        raise RuntimeError("Please install: pip install edge-tts")

    chunks, wbs = [], []

    async def _run():
        com = edge_tts.Communicate(text, voice=voice, rate=rate)
        async for chunk in com.stream():
            if chunk["type"] == "audio":
                chunks.append(chunk["data"])
            elif chunk["type"] == "WordBoundary":
                wbs.append(chunk)

    loop = asyncio.new_event_loop()
    loop.run_until_complete(_run())
    loop.close()

    audio = b"".join(chunks)

    # edge_tts WordBoundary offset unit: 100ns
    words = []
    for wb in wbs:
        s = wb["offset"] / 1e7
        e = (wb["offset"] + wb["duration"]) / 1e7
        words.append({"word": wb["text"], "start": round(s, 3), "end": round(e, 3)})

    dur = words[-1]["end"] if words else 0.0
    segs = words_to_segs(words)

    if precise:
        from stt import stt_local

        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp:
            tmp.write(audio)
            path = tmp.name
        try:
            local = stt_local(path, "", "base")
            words, segs, dur = local["words"], local["segments"], local["duration"]
        except Exception as ex:
            print(f"[precise] Whisper correction failed, falling back to edge_tts timestamps: {ex}")
        finally:
            os.unlink(path)

    return {
        "audio_base64": base64.b64encode(audio).decode(),
        "audio_format": "mp3",
        "words": words,
        "segments": segs,
        "duration": round(dur or 0, 3),
    }
