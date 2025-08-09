import re
from moviepy import *
from __init__ import *

#画像クリップを生成
def image(current_time, start_time, path):
    img_clip = ImageClip(f"images/{path}").with_duration(current_time - start_time).with_start(start_time)
    
    # 画面にフィットするように拡大（どちらかが大きくなる）
    img_clip = img_clip.resized(lambda t: max(1920 / img_clip.w, 1080 / img_clip.h))
    
    # 中心からクロップして1920x1080にする
    img_clip = img_clip.cropped(x_center=img_clip.w / 2,
                             y_center=img_clip.h / 2,
                             width=1920, height=1080)
    img_clip = img_clip.with_position(('center', 'center'))
    return img_clip

#期間中の背景画像の生成
def image_overlay(**kwargs):

    path = kwargs.get('path')
    duration = float(kwargs.get('duration', 3))
    position = kwargs.get('position', 'center') # 位置のデフォルトは中央

    if not path:
        print("エラー: インラインのimageコマンドにはpathが必要です。")
        return None
    
    try:
        # 画像を読み込み、長さと位置を設定
        clip = ImageClip(f"images/{path}").with_duration(duration).with_position(position)
        return clip
    except Exception as e:
        print(f"エラー: 画像 '{path}' の読み込みに失敗しました。 {e}")
        return None
    
    
#タイトルクリップを生成
def title(**kwargs):
    config = kwargs.get('config', Config())
    text = kwargs.get('text', ' ')
    duration = float(kwargs.get('duration', 3))
    clip = TextClip(text=text, font_size=config.TITLE_FONT_SIZE, color=config.TITLE_FONT_COLOR, font=config.TITLE_FONT, size=(1700, 300)).with_duration(duration)
    clip = clip.with_position(('center', 'center'))
    print(f"タイトルクリップを生成: テキスト='{text}', フォントサイズ={config.TITLE_FONT_SIZE}, 色={config.TITLE_FONT_COLOR}")
    return clip

#SEクリップを生成
def se(**kwargs):
    path = kwargs.get('path', 'default_se.wav')
    volume = float(kwargs.get('volume', 0.7))
    se = AudioFileClip(f"sounds/{path}").with_volume_scaled(volume)
    background = ColorClip(size=(1920, 1080), color=(0, 0, 0)).with_duration(se.duration).with_opacity(0)
    se = background.with_audio(se)      
    print(f"SEクリップを生成: パス='{path}', ボリューム={volume}")
    return se

def bgm(current_time, start_time, kwargs):
    path = kwargs.get('path', 'default_bgm.mp3')
    volume = float(kwargs.get('volume', 0.2))
    bgm_clip = AudioFileClip(f"sounds/{path}").with_volume_scaled(volume)
    bgm_loop = bgm_clip.with_effects([afx.AudioLoop(duration=current_time - start_time)])
    background = ColorClip(size=(1920, 1080), color=(0, 0, 0)).with_duration(bgm_loop.duration).with_opacity(0)
    bgm_clip = background.with_audio(bgm_loop).with_start(start_time)
    print(f"BGMクリップを生成: パス='{path}', ボリューム={volume}, 開始時間={start_time}, 現在の時間={current_time}")
    return bgm_clip

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
def set_talk(**kwargs):
    config = kwargs.get('config', Config())
    config.TALK_SPEED = float(kwargs.get('speed', config.TALK_SPEED))
    config.SILENCE_DURATION = float(kwargs.get('silence_duration', config.SILENCE_DURATION))
    config.SPEAKERS[0] = int(kwargs.get('talker1',1))
    config.SPEAKERS[1] = int(kwargs.get('talker2',2))
    print(f"話すスピードを更新: スピード={config.TALK_SPEED}, 無音時間={config.SILENCE_DURATION}, トーカー1={config.SPEAKERS[0]}, トーカー2={config.SPEAKERS[1]}")
    