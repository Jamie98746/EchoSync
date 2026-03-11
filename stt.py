"""Speech-to-text (STT) related functionality."""

from openai_client import _openai
from whisper_singleton import _whisper


def stt_cloud(path: str, lang: str):
    c = _openai()
    with open(path, "rb") as f:
        r = c.audio.transcriptions.create(
            model="whisper-1",
            file=f,
            language=lang or None,
            response_format="verbose_json",
            timestamp_granularities=["word", "segment"],
        )

    words, segs = [], []
    for w in (r.words or []):
        words.append({"word": w.word, "start": round(w.start, 3), "end": round(w.end, 3)})
    for s in (r.segments or []):
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
    return {
        "text": r.text,
        "words": words,
        "segments": segs,
        "duration": getattr(r, "duration", None),
    }


def stt_local(path: str, lang: str, size: str = "base"):
    model = _whisper(size)
    result = model.transcribe(path, language=lang or None, word_timestamps=True, verbose=False)

    words, segs = [], []
    for seg in result.get("segments", []):
        sw = []
        for w in seg.get("words", []):
            e = {"word": w["word"].strip(), "start": round(w["start"], 3), "end": round(w["end"], 3)}
            words.append(e)
            sw.append(e)
        segs.append({
            "text": seg["text"].strip(),
            "start": round(seg["start"], 3),
            "end": round(seg["end"], 3),
            "words": sw,
        })

    dur = segs[-1]["end"] if segs else None
    return {
        "text": result["text"].strip(),
        "words": words,
        "segments": segs,
        "duration": round(dur, 3) if dur else None,
    }
