# 声文同期 · SyncLyric

📌 **音声 ↔ テキスト 双方向同期（カラオケ風歌詞ハイライト）**

> **☁️ クラウドモード**（OpenAI API）と **💻 ローカルモード**（openai-whisper + edge-tts）をサポートし、**日/英/中 UI 切り替え**が可能です。

---

## ✨ 主な機能

- **音声→テキスト（STT）**
  - ☁️ クラウド：OpenAI Whisper API（単語レベルのタイムスタンプ対応）
  - 💻 ローカル：openai-whisper（オフライン、モデルサイズ選択可）
- **テキスト→音声（TTS）**
  - ☁️ クラウド：OpenAI TTS（6種類の音声内蔵）
  - 💻 ローカル：edge-tts（Microsoft Azure ニューラル、無料）
- **歌詞同期ハイライト**（再生に合わせて自動スクロール＆現在の単語を強調表示）
- **多言語 UI**：中 / 英 / 日（ブラウザ言語自動検出 + 手動切替）
- **リアルタイム機能チェック**：OpenAI Key、Whisper、edge-tts、ffmpeg の状態を検出

---

## 🚀 クイックスタート

### 1) 依存関係のインストール

```bash
pip install flask flask-cors

# クラウドモード
pip install openai

# ローカルモード STT
pip install openai-whisper
# pip install torch   # CPU版はCPU用のwhlを指定してインストールすることを推奨

# ローカルモード TTS
pip install edge-tts
```

### 2) （クラウドモード時）OPENAI_API_KEY を設定

```bash
export OPENAI_API_KEY=sk-xxx            # macOS / Linux
set OPENAI_API_KEY=sk-xxx                # Windows CMD
$env:OPENAI_API_KEY="sk-xxx"           # PowerShell
```

### 3) サービスを起動

```bash
python server.py
```

ブラウザで開く：<http://localhost:5000>

---

## 🌐 多言語対応

- ブラウザ言語に基づいて自動的に切り替わります（`zh` / `ja` 対応、その他は `en` になります）
- 右上の言語ドロップダウンで手動切替も可能
- 切り替えると UI テキスト、TTS 音声説明、Whisper モデル説明が自動更新されます

---

## 🔌 API 説明

### GET `/api/capabilities`
必要な依存関係が利用可能か（OpenAI API、Whisper、edge-tts、ffmpeg など）を検出します。

### GET `/api/edge_voices`
現在の言語で利用可能な edge-tts ボイスのリストを返します。

### GET `/api/whisper_models`
現在の言語用の Whisper モデル説明リストを返します。

### POST `/api/transcribe`
form-data パラメータ：

| パラメータ | 説明 | デフォルト |
|------------|------|------------|
| audio | 音声ファイル | 必須 |
| language | 言語コード（zh/en/ja/ko）、空=自動検出 | zh |
| mode | cloud / local | cloud |
| model_size | ローカルモード時（tiny/base/small/medium/large） | base |

### POST `/api/synthesize`
JSON パラメータ：

| パラメータ | 説明 | デフォルト |
|------------|------|------------|
| text | 合成するテキスト | 必須 |
| mode | cloud / local | cloud |
| **cloud** | | |
| voice | alloy/echo/fable/onyx/nova/shimmer | nova |
| speed | 0.5~2.0 | 1.0 |
| model | tts-1 / tts-1-hd | tts-1 |
| precise | true=Whisper で再トランスクリプトして正確なタイムスタンプ | false |
| **local** | | |
| edge_voice | 例：zh-CN-XiaoxiaoNeural | zh-CN-XiaoxiaoNeural |
| rate | +0% / +10% / -20% など | +0% |
| local_precise | true=ローカルWhisperでタイムスタンプ補正 | false |

---

## 📁 プロジェクト構成

```
EchoSync/
├── server.py          # Flask バックエンド（クラウド + ローカルのデュアルモード）
├── routes.py          # Flask ルート（多言語 TTS/Whisper モデルオプション含む）
├── consts.py          # ローカライズされた TTS 言語名 + Whisper モデル説明
├── stt.py             # STT 実装（クラウド/ローカル）
├── tts.py             # TTS 実装（クラウド/ローカル）
├── static/
│   └── index.html     # シングルページフロントエンド（多言語 UI、歌詞同期）
├── requirements.txt
└── README.md
```

---

## ✅ よくある質問

- **ページの言語が変わりません。**
  - 右上の言語ドロップダウンから選択し、リロードしてください（localStorage に保存されます）。

- **ローカルモードがインストールされていないと表示されるのはなぜ？**
  - `openai-whisper`（STT）、および/または `edge-tts`（TTS）をインストールし、`ffmpeg` が使用可能であることを確認してください。

- **ローカルで高精度タイムスタンプを使うには？**
  - ローカルモードで「精密タイムスタンプ」オプションを有効にすると、Whisper で再トランスクリプトしてタイミングを改善します。
