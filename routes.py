"""Flask route definitions.

All API routes are defined in this module, while server.py only creates the app and registers routes.
"""

import os
import time
import tempfile

from flask import jsonify, request, send_from_directory

from capabilities import get_capabilities
from consts import EDGE_VOICES, WHISPER_MODELS
from stt import stt_cloud, stt_local
from tts import tts_cloud, tts_local


def register_routes(app):
    @app.route("/api/capabilities")
    def capabilities():
        return jsonify(get_capabilities())

    @app.route("/api/edge_voices")
    def edge_voices():
        lang = request.args.get('lang', 'en')
        return jsonify(EDGE_VOICES.get(lang, EDGE_VOICES.get('en', {})))

    @app.route("/api/whisper_models")
    def whisper_models():
        lang = request.args.get('lang', 'en')
        return jsonify(WHISPER_MODELS.get(lang, WHISPER_MODELS.get('en', {})))

    @app.route("/api/transcribe", methods=["POST"])
    def transcribe():
        """form-data: audio, language, mode(cloud|local), model_size(tiny/base/small/medium/large)"""
        if "audio" not in request.files:
            return jsonify({"error": "Missing audio file"}), 400

        f = request.files["audio"]
        lang = request.form.get("language", "zh")
        mode = request.form.get("mode", "cloud")
        size = request.form.get("model_size", "base")

        suffix = os.path.splitext(f.filename)[1] or ".mp3"
        with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
            f.save(tmp.name)
            path = tmp.name
        try:
            result = stt_local(path, lang, size) if mode == "local" else stt_cloud(path, lang)
            return jsonify(result)
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        finally:
            os.unlink(path)

    @app.route("/api/synthesize", methods=["POST"])
    def synthesize():
        """JSON:
          mode: cloud | local
          text, [cloud] voice/speed/model/precise, [local] edge_voice/rate/local_precise
        """
        d = request.get_json(force=True)
        text = d.get("text", "").strip()
        mode = d.get("mode", "cloud")
        if not text:
            return jsonify({"error": "text is required"}), 400

        try:
            if mode == "local":
                res = tts_local(
                    text,
                    d.get("edge_voice", "zh-CN-XiaoxiaoNeural"),
                    d.get("rate", "+0%"),
                    bool(d.get("local_precise", False)),
                )
            else:
                res = tts_cloud(
                    text,
                    d.get("voice", "nova"),
                    float(d.get("speed", 1.0)),
                    d.get("model", "tts-1"),
                    bool(d.get("precise", False)),
                )
            return jsonify(res)
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route("/")
    def index():
        return send_from_directory("static", "index.html")

    @app.route("/health")
    def health():
        return jsonify({"status": "ok", "time": time.time()})
