"""OpenAI 客户端封装。"""

import os


def _openai():
    try:
        from openai import OpenAI
    except ImportError:
        raise RuntimeError("请安装 openai: pip install openai")
    key = os.environ.get("OPENAI_API_KEY", "").strip()
    if not key:
        raise RuntimeError("请设置环境变量 OPENAI_API_KEY")
    return OpenAI(api_key=key)
