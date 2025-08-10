import os
import signal
from compiler import analyze_text

def preview_worker(text, talk_mode, is_green_mode):
    """動画プレビューを別プロセスで実行するワーカ関数"""
    clip = analyze_text(text, talk_mode, is_green_mode)
    if clip is None:
        return
    clip = clip.resized((896, 504)).with_fps(3)
    try:
        clip.preview(fps=3, audio_fps=11100)
    except OSError:
        os.kill(os.getpid(), signal.SIGTERM)
