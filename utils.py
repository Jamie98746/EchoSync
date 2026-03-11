"""Utility helper functions."""

import re


def words_to_segs(words):
    """Convert a list of timed words into sentence/segment-level timestamps."""
    punc = re.compile(r'[，。！？；,.!?;\n]')
    segs, buf, txt = [], [], ""
    for w in words:
        buf.append(w)
        txt += w["word"]
        if punc.search(w["word"]):
            segs.append({
                "text": txt.strip(),
                "start": buf[0]["start"],
                "end": buf[-1]["end"],
                "words": list(buf),
            })
            buf, txt = [], ""
    if buf:
        segs.append({
            "text": txt.strip(),
            "start": buf[0]["start"],
            "end": buf[-1]["end"],
            "words": list(buf),
        })
    return segs


def estimate_ts(text, speed=1.0):
    """Roughly estimate text-to-speech timestamps (engine-independent)."""
    zh = len(re.findall(r'[\u4e00-\u9fff]', text)) / max(len(text), 1) > 0.3
    cps = (3.5 if zh else 14.0) * speed
    tot_c, tot_s = max(len(text), 1), max(len(text), 1) / cps
    toks = list(text) if zh else text.split()
    words, cur = [], 0.0
    for t in toks:
        if not t.strip():
            continue
        d = len(t) / tot_c * tot_s
        words.append({"word": t, "start": round(cur, 3), "end": round(cur + d, 3)})
        cur += d

    pat = r'([，。！？；\n])' if zh else r'([,\.\!\?;\n])'
    segs, c2, buf = [], 0.0, ""
    for p in re.split(pat, text):
        if not p:
            continue
        sd = len(p) / tot_c * tot_s
        is_p = bool(re.match(r'^[，。！？；,\.\!\?;\n]$', p))
        buf += p
        if is_p and buf.strip():
            segs.append({"text": buf.strip(), "start": round(c2, 3), "end": round(c2 + sd, 3), "words": []})
            c2 += sd
            buf = ""
        elif not is_p:
            c2 += sd
    if buf.strip():
        segs.append({"text": buf.strip(), "start": round(c2, 3), "end": round(tot_s, 3), "words": []})
    return {"words": words, "segments": segs, "duration": round(tot_s, 3)}
