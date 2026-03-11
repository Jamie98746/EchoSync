"""Audio-to-text & text-to-audio server.

Supports local mode (openai-whisper + edge_tts) and cloud mode (OpenAI API).

Dependencies:
    pip install flask flask-cors openai          # cloud
    pip install openai-whisper edge-tts torch    # local (additional)

Usage:
    python server.py  →  open http://localhost:5000
"""

import os
import time

from flask import Flask
from flask_cors import CORS

from routes import register_routes

app = Flask(__name__, static_folder="static")
CORS(app)

register_routes(app)


if __name__ == "__main__":
    print("🎵 EchoSync server")
    print("  Cloud mode: set OPENAI_API_KEY")
    print("  Local mode: pip install openai-whisper edge-tts torch")
    print("  Open: http://localhost:5000")
    app.run(debug=True, host="0.0.0.0", port=5000)
