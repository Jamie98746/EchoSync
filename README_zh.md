# 声文同步 · SyncLyric

[![中文](https://img.shields.io/badge/lang-中文-red)](README_zh.md) [![English](https://img.shields.io/badge/lang-English-blue)](README.en.md) [![日本語](https://img.shields.io/badge/lang-日本語-green)](README.ja.md)

📌 **Audio ↔ Text 双向同步（歌词卡拉OK式高亮）**

> 支持 **☁️ 云端模式**（OpenAI API）和 **💻 本地模式**（openai-whisper + edge-tts），并且支持 **中/英/日三语界面切换**。

---

## ✨ 主要功能

- **语音转文本（STT）**
  - ☁️ 云端：OpenAI Whisper API（支持词级时间戳）
  - 💻 本地：openai-whisper（离线，可选模型大小）
- **文本转语音（TTS）**
  - ☁️ 云端：OpenAI TTS（内置 6 种音色）
  - 💻 本地：edge-tts（微软 Azure 神经网络，免费）
- **歌词同步高亮**（播放时跟随时间自动滚动并高亮当前词）
- **多语言 UI**：中 / 英 / 日（自动检测浏览器语言 + 手动切换）
- **实时能力检测**：检测 OpenAI Key、Whisper、edge-tts、ffmpeg 状态

---

## 🚀 快速启动

### 1) 安装依赖

```bash
pip install flask flask-cors

# 云端模式
pip install openai

# 本地模式 STT
pip install openai-whisper
# pip install torch   # CPU 版推荐指定 CPU whl

# 本地模式 TTS
pip install edge-tts
```

### 2) (云端模式需要) 设置 OPENAI_API_KEY

```bash
export OPENAI_API_KEY=sk-xxx            # macOS / Linux
set OPENAI_API_KEY=sk-xxx                # Windows CMD
$env:OPENAI_API_KEY="sk-xxx"           # PowerShell
```

### 3) 运行服务

```bash
python server.py
```

打开浏览器访问：<http://localhost:5000>

---

## 🌐 多语言支持

- 默认根据浏览器语言自动切换（支持 `zh` / `ja`，其它默认 `en`）
- 也可通过页面右上角“语言”下拉手动切换
- 切换时 UI 文本、TTS 音色描述、Whisper 模型说明都会自动刷新

---

## 🔌 API 说明

### GET `/api/capabilities`
检测当前环境依赖是否可用（OpenAI API、Whisper、edge-tts、ffmpeg 等）。

### GET `/api/edge_voices`
返回当前语言下的 edge-tts 可用语音列表。

### GET `/api/whisper_models`
返回当前语言下的 Whisper 模型说明列表。

### POST `/api/transcribe`
form-data 参数：

| 参数 | 说明 | 默认 |
|------|------|------|
| audio | 音频文件 | 必填 |
| language | 语言代码（zh/en/ja/ko），空 = 自动检测 | zh |
| mode | cloud / local | cloud |
| model_size | local 模式时（tiny/base/small/medium/large） | base |

### POST `/api/synthesize`
JSON 参数：

| 参数 | 说明 | 默认 |
|------|------|------|
| text | 要合成的文本 | 必填 |
| mode | cloud / local | cloud |
| **cloud** | | |
| voice | alloy/echo/fable/onyx/nova/shimmer | nova |
| speed | 0.5~2.0 | 1.0 |
| model | tts-1 / tts-1-hd | tts-1 |
| precise | true=Whisper 反转录精确时间戳 | false |
| **local** | | |
| edge_voice | 如 zh-CN-XiaoxiaoNeural | zh-CN-XiaoxiaoNeural |
| rate | +0% / +10% / -20% 等 | +0% |
| local_precise | true=本地 Whisper 校正时间戳 | false |

---

## 📁 项目结构

```
EchoSync/
├── server.py          # Flask 后端（云端 + 本地双模式）
├── routes.py          # Flask 路由（含多语言 TTS/Whisper 模型选项）
├── consts.py          # 语言化的 TTS 语言名称 + Whisper 模型说明
├── stt.py             # STT 实现（云端/本地）
├── tts.py             # TTS 实现（云端/本地）
├── static/
│   └── index.html     # 单页前端（含多语言 UI、歌词同步）
├── requirements.txt
└── README.md
```

---

## ✅ 常见问题

- **为什么页面语言没变？**
  - 请在右上角语言下拉选择后刷新（会自动保存至 localStorage）。

- **为什么本地模式提示未安装？**
  - 需要安装 `openai-whisper`（STT）和/或 `edge-tts`（TTS），并确保 `ffmpeg` 可用。

- **如何使用本地高精度时间戳？**
  - 在本地模式下开启“精确时间戳”选项，会通过 Whisper 重新转录来优化时间点。
