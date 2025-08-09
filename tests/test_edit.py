import re
from moviepy import *
from __init__ import *
import os

#画像クリップを生成
def image(current_time, start_time, path):
    if not os.path.exists(f"images/{path}"):
        print(f"エラー: ファイルが見つかりません_{path}")
        return None
    
    img_clip = ImageClip(f"images/{path}").with_duration(current_time - start_time).with_start(start_time)
    '''
    # 画面にフィットするように拡大（どちらかが大きくなる）
    img_clip = img_clip.resized(lambda t: max(1920 / img_clip.w, 1080 / img_clip.h))

    # 中心からクロップして1920x1080にする
    img_clip = img_clip.cropped(x_center=img_clip.w / 2,
                                y_center=img_clip.h / 2,
                                width=1920, height=1080)
    '''
    img_clip = img_clip.with_position(('center', 'center'))
    print(f"画像クリップを生成: パス='{path}', 開始時間={start_time}, 終了時間={current_time}")
    return img_clip
    
#タイトルクリップを生成
def title(**kwargs):
    config = kwargs.get('config', Config())
    text = kwargs.get('text', ' ')
    duration = float(kwargs.get('duration', 3))
    try:
        clip = TextClip(text=text, font_size=config.TITLE_FONT_SIZE, color=config.TITLE_FONT_COLOR, stroke_color=config.TITLE_FONT_STROKE_COLOR, stroke_width=config.TITLE_FONT_STROKE_WIDTH, font=config.TITLE_FONT, size=(1700, 600)).with_duration(duration)
        print(f"タイトルクリップを生成: テキスト='{text}', フォントサイズ={config.TITLE_FONT_SIZE}, 色={config.TITLE_FONT_COLOR}, ストローク色={config.TITLE_FONT_STROKE_COLOR}, ストローク幅={config.TITLE_FONT_STROKE_WIDTH}")
        return clip.with_position(('center', 'center'))
    except Exception as e:
        print(f"エラー:タイトルクリップの生成に失敗_{e}")
        return None


#SEクリップを生成
def se(**kwargs):
    path = kwargs['path']
    volume = float(kwargs.get('volume', 0.7))
    
    if not os.path.exists(f"sounds/{path}"):
        print(f"エラー: ファイルが見つかりません_{path}")
        return None

    se = AudioFileClip(f"sounds/{path}").with_volume_scaled(volume)
    background = ColorClip(size=(1920, 1080), color=(0, 0, 0)).with_duration(se.duration).with_opacity(0)
    se = background.with_audio(se) 
    print(f"SEクリップを生成: パス='{path}', ボリューム={volume}")
    return se

def bgm(current_time, start_time, kwargs):
    path = kwargs['path']
    volume = float(kwargs.get('volume', 0.2))
    
    if not os.path.exists(f"sounds/{path}"):
        print(f"エラー: ファイルが見つかりません_{path}")
        return None
    
    bgm_clip = AudioFileClip(f"sounds/{path}").with_volume_scaled(volume)
    bgm_loop = bgm_clip.with_effects([afx.AudioLoop(duration=current_time - start_time)])
    background = ColorClip(size=(1920, 1080), color=(0, 0, 0)).with_duration(bgm_loop.duration).with_opacity(0)
    bgm_clip = background.with_audio(bgm_loop).with_start(start_time)
    print(f"BGMクリップを生成: パス='{path}', ボリューム={volume}, 開始時間={start_time}, 終了時間={current_time}")
    return bgm_clip

#字幕設定を更新
def set_subtitle(**kwargs):
    config = kwargs.get('config', Config())
    config.SUBTITLE_FONT_SIZE = int(kwargs.get('size', config.SUBTITLE_FONT_SIZE))
    config.SUBTITLE_FONT_COLOR[0] = kwargs.get('color', config.SUBTITLE_FONT_COLOR[0])
    config.SUBTITLE_FONT_STROKE_COLOR[0] = kwargs.get('stroke_color', config.SUBTITLE_FONT_STROKE_COLOR[0])
    config.SUBTITLE_FONT_COLOR[0] = kwargs.get('color1', config.SUBTITLE_FONT_COLOR[0])
    config.SUBTITLE_FONT_STROKE_COLOR[0] = kwargs.get('stroke_color1', config.SUBTITLE_FONT_STROKE_COLOR[0])
    config.SUBTITLE_FONT_COLOR[1] = kwargs.get('color2', config.SUBTITLE_FONT_COLOR[1])
    config.SUBTITLE_FONT_STROKE_COLOR[1] = kwargs.get('stroke_color2', config.SUBTITLE_FONT_STROKE_COLOR[1])
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
def set_talk(**kwargs):
    config = kwargs.get('config', Config())
    config.TALK_SPEED = float(kwargs.get('speed', config.TALK_SPEED))
    config.SILENCE_DURATION = float(kwargs.get('silence_duration', config.SILENCE_DURATION))
    config.SPEAKERS[0] = int(kwargs.get('talker1',config.SPEAKERS[0]))
    config.SPEAKERS[1] = int(kwargs.get('talker2',config.SPEAKERS[1]))
    print(f"話すスピードを更新: スピード={config.TALK_SPEED}, 無音時間={config.SILENCE_DURATION}, 話者1={config.SPEAKERS[0]}, 話者2={config.SPEAKERS[1]}")
    