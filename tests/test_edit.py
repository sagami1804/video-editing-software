import re
from moviepy import *

def image(path):
     #画像クリップを生成
     try:
        return ImageClip(path).set_duration(duration)
     except Exception as e:
        return None
     
def section(text, duration):
    #セクションタイトル（テロップ）を生成
    return TextClip(text, fontsize=70, color='white', font='Arial-Bold').set_duration(duration)

def delay(duration):
    #無音クリップ（間）を生成
    return ColorClip(size=(1, 1), color=(0, 0, 0), duration=duration)

