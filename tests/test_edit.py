import re
from moviepy import *
from __init__ import *

#画像クリップを生成
def image(current_time, start_time, path):
    img_clip = ImageClip(path).with_duration(current_time - start_time).with_start(start_time)
    img_clip = img_clip.with_position(('center', 'center'))
    return img_clip
    
#タイトルクリップを生成
def title(**kwargs):
    config = kwargs.get('config', Config())
    text = kwargs.get('text', ' ')
    duration = float(kwargs.get('duration', 3))
    clip = TextClip(text=text, font_size=config.TITLE_FONT_SIZE, color=config.TITLE_FONT_COLOR, font=config.TITLE_FONT, size=(1700, 300)).with_duration(duration)
    clip = clip.with_position(('center', 'center'))
    return clip

#字幕設定を更新
def set_subtitle(**kwargs):
    config = kwargs.get('config', Config())
    config.SUBTITLE_FONT_SIZE = int(kwargs.get('size', config.SUBTITLE_FONT_SIZE))
    config.SUBTITLE_FONT_COLOR = kwargs.get('color', config.SUBTITLE_FONT_COLOR)
    config.SUBTITLE_FONT_STROKE_COLOR = kwargs.get('stroke_color', config.SUBTITLE_FONT_STROKE_COLOR)
    config.SUBTITLE_FONT_STROKE_WIDTH = int(kwargs.get('stroke_width', config.SUBTITLE_FONT_STROKE_WIDTH))
    print(f"字幕の設定を更新: フォントサイズ={config.SUBTITLE_FONT_SIZE}, 色={config.SUBTITLE_FONT_COLOR}, ストローク色={config.SUBTITLE_FONT_STROKE_COLOR}, ストローク幅={config.SUBTITLE_FONT_STROKE_WIDTH}")
    
#タイトル設定を更新
def set_title(**kwargs):
    config = kwargs.get('config', Config())
    config.TITLE_FONT_SIZE = int(kwargs.get('size', config.TITLE_FONT_SIZE))
    config.TITLE_FONT_COLOR = kwargs.get('color', config.TITLE_FONT_COLOR)
    config.TITLE_FONT_STROKE_COLOR = kwargs.get('stroke_color', config.TITLE_FONT_STROKE_COLOR)
    config.TITLE_FONT_STROKE_WIDTH = int(kwargs.get('stroke_width', config.TITLE_FONT_STROKE_WIDTH))
    print(f"タイトルの設定を更新: フォントサイズ={config.TITLE_FONT_SIZE}, 色={config.TITLE_FONT_COLOR}, ストローク色={config.TITLE_FONT_STROKE_COLOR}, ストローク幅={config.TITLE_FONT_STROKE_WIDTH}")

# 話すスピードを設定
def set_talk_speed(speed=1.0,config=Config()):
    config.TALK_SPEED = float(speed)
    print(f"話すスピードを設定: {config.TALK_SPEED}")
    