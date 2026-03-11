# SyncLyric

[![中文](https://img.shields.io/badge/lang-中文-red)](README_zh.md) [![English](https://img.shields.io/badge/lang-English-blue)](README.en.md) [![日本語](https://img.shields.io/badge/lang-日本語-green)](README.ja.md)

📌 **Audio ↔ Text bidirectional synchronization (karaoke-style lyric highlighting)**

> Supports **☁️ Cloud mode** (OpenAI API) and **💻 Local mode** (openai-whisper + edge-tts), with **Chinese/English/Japanese UI switching**.

---

## ✨ Key Features

- **Speech-to-Text (STT)**
  - ☁️ Cloud: OpenAI Whisper API (supports word-level timestamps)
  - 💻 Local: openai-whisper (offline, selectable model sizes)
- **Text-to-Speech (TTS)**
  - ☁️ Cloud: OpenAI TTS (6 built-in voices)
  - 💻 Local: edge-tts (Microsoft Azure neural voices, free)
- **Lyric synchronization highlighting** (auto-scrolls and highlights current words during playback)
- **Multilingual UI**: Chinese / English / Japanese (auto-detect browser language + manual switch)
- **Real-time capability check**: detects OpenAI Key, Whisper, edge-tts, ffmpeg status

---

## 🚀 Quick Start

### 1) Install dependencies

```bash
pip install flask flask-cors

# Cloud mode
pip install openai

# Local mode STT
pip install openai-whisper
# pip install torch   # For CPU-only: pip install torch --index-url https://download.pytorch.org/whl/cpu

# Local mode TTS
pip install edge-tts
```

### 2) (Cloud mode only) Set OPENAI_API_KEY

```bash
export OPENAI_API_KEY=sk-xxx            # macOS / Linux
set OPENAI_API_KEY=sk-xxx                # Windows CMD
$env:OPENAI_API_KEY="sk-xxx"           # PowerShell
```

### 3) Run the service

```bash
python server.py
```

Open the browser at: <http://localhost:5000>

---

## 🌐 Multilingual Support

- Automatically switches based on browser language (supports `zh` / `ja`, others default to `en`)
- You can also switch manually via the language dropdown in the top-right corner
- When switching, UI text, TTS voice descriptions, and Whisper model descriptions refresh automatically

---

## 🔌 API Reference

### GET `/api/capabilities`
Checks whether required dependencies are available (OpenAI API, Whisper, edge-tts, ffmpeg, etc.).

### GET `/api/edge_voices`
Returns the list of available edge-tts voices for the current language.

### GET `/api/whisper_models`
Returns the list of Whisper model descriptions for the current language.

### POST `/api/transcribe`
Form-data parameters:

| Parameter | Description | Default |
|-----------|-------------|---------|
| audio | Audio file | required |
| language | Language code (zh/en/ja/ko), empty = auto-detect | zh |
| mode | cloud / local | cloud |
| model_size | Local mode only (tiny/base/small/medium/large) | base |

### POST `/api/synthesize`
JSON parameters:

| Parameter | Description | Default |
|-----------|-------------|---------|
| text | Text to synthesize | required |
| mode | cloud / local | cloud |
| **cloud** | | |
| voice | alloy/echo/fable/onyx/nova/shimmer | nova |
| speed | 0.5~2.0 | 1.0 |
| model | tts-1 / tts-1-hd | tts-1 |
| precise | true = Whisper reverse-transcription for precise timestamps | false |
| **local** | | |
| edge_voice | e.g. zh-CN-XiaoxiaoNeural | zh-CN-XiaoxiaoNeural |
| rate | +0% / +10% / -20% etc | +0% |
| local_precise | true = local Whisper timestamp correction | false |

---

## 📁 Project Structure

```
EchoSync/
├── server.py          # Flask backend (cloud + local dual mode)
├── routes.py          # Flask routes (includes multilingual TTS/Whisper model options)
├── consts.py          # Localized TTS language names + Whisper model descriptions
├── stt.py             # STT implementation (cloud/local)
├── tts.py             # TTS implementation (cloud/local)
├── static/
│   └── index.html     # Single-page frontend (multilingual UI, lyric sync)
├── requirements.txt
└── README.md
```

---

## ✅ FAQ

- **Why didn’t the page language change?**
  - Please select the language from the top-right dropdown and refresh (it is saved to localStorage).

- **Why does local mode say it is not installed?**
  - You need to install `openai-whisper` (STT) and/or `edge-tts` (TTS), and make sure `ffmpeg` is available.

- **How do I enable high-precision timestamps locally?**
  - In local mode, enable the “precise timestamps” option, which re-transcribes with Whisper to improve timing.
