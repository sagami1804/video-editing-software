import re
from moviepy import *
#画像クリップを生成
def image(**kwargs):
    path = kwargs.get('path')
    duration = float(kwargs.get('duration'))
    try:
        return ImageClip(path)
    except Exception as e:
        return None
    
#セクションタイトル（テロップ）を生成
def section(**kwargs):
    text = kwargs.get('text', ' ')
    duration = float(kwargs.get('duration', 3))
    clip = TextClip(text=text, font_size=70, color='white', font="fonts/Corporate-Logo-Rounded-Bold-ver3.otf").with_duration(duration)
    return clip

#無音の「音声クリップ」を生成
def delay(**kwargs):
    duration = float(kwargs.get('duration', 1))
    
    return AudioClip(lambda t: 0, duration=duration)

section(text="セクションタイトル", duration=3)