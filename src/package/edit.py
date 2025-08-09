import os
import ast
from moviepy import *
from __init__ import *

# ------------------------------------------------------------
# 画像クリップ生成
# ------------------------------------------------------------
def image(current_time, start_time, path):
    """
    画像ファイルから ImageClip を生成する。
    
    Args:
        current_time (float): クリップ終了時刻（秒）
        start_time (float): クリップ開始時刻（秒）
        path (str): 画像ファイル名（images ディレクトリ内）
    
    Returns:
        ImageClip | None: 成功時は ImageClip、失敗時は None
    """
    img_path = f"images/{path}"
    if not os.path.exists(img_path):
        print(f"[エラー] ファイルが見つかりません: {path}")
        return None

    img_clip = ImageClip(img_path) \
        .with_duration(current_time - start_time) \
        .with_start(start_time) \
        .with_position(('center', 'center'))

    # 必要に応じて拡大・クロップする場合は以下を有効化
    """
    img_clip = img_clip.resized(lambda t: max(1920 / img_clip.w, 1080 / img_clip.h))
    img_clip = img_clip.cropped(
        x_center=img_clip.w / 2,
        y_center=img_clip.h / 2,
        width=1920, height=1080
    )
    """

    print(f"[画像生成] パス='{path}', 開始={start_time}, 終了={current_time}")
    return img_clip


# ------------------------------------------------------------
# タイトルクリップ生成
# ------------------------------------------------------------
def title(**kwargs):
    config = kwargs.get('config', Config())
    text = kwargs.get('text', ' ')
    duration = float(kwargs.get('duration', 3))

    try:
        clip = TextClip(
            text=text,
            font_size=config.TITLE_FONT_SIZE,
            color=config.TITLE_FONT_COLOR,
            stroke_color=config.TITLE_FONT_STROKE_COLOR,
            stroke_width=config.TITLE_FONT_STROKE_WIDTH,
            font=config.TITLE_FONT,
            size=(1700, 600)
        ).with_duration(duration).with_position(('center', 'center'))

        print(f"[タイトル生成] '{text}' / size={config.TITLE_FONT_SIZE}, color={config.TITLE_FONT_COLOR}")
        return clip
    except Exception as e:
        print(f"[エラー] タイトル生成失敗: {e}")
        return None


# ------------------------------------------------------------
# SEクリップ生成
# ------------------------------------------------------------
def se(**kwargs):
    path = kwargs['path']
    volume = float(kwargs.get('volume', 0.7))
    se_path = f"sounds/{path}"

    if not os.path.exists(se_path):
        print(f"[エラー] ファイルが見つかりません: {path}")
        return None

    audio = AudioFileClip(se_path).with_volume_scaled(volume)
    background = ColorClip(size=(1920, 1080), color=(0, 0, 0)) \
        .with_duration(audio.duration).with_opacity(0)
    
    clip = background.with_audio(audio)
    print(f"[SE生成] '{path}', volume={volume}")
    return clip


# ------------------------------------------------------------
# BGMクリップ生成
# ------------------------------------------------------------
def bgm(current_time, start_time, kwargs):
    path = kwargs['path']
    volume = float(kwargs.get('volume', 0.2))
    bgm_path = f"sounds/{path}"

    if not os.path.exists(bgm_path):
        print(f"[エラー] ファイルが見つかりません: {path}")
        return None

    bgm_clip = AudioFileClip(bgm_path).with_volume_scaled(volume)
    loop_clip = bgm_clip.with_effects([afx.AudioLoop(duration=current_time - start_time)])

    background = ColorClip(size=(1920, 1080), color=(0, 0, 0)) \
        .with_duration(loop_clip.duration).with_opacity(0)

    final_clip = background.with_audio(loop_clip).with_start(start_time)
    print(f"[BGM生成] '{path}', volume={volume}, start={start_time}, end={current_time}")
    return final_clip


# ------------------------------------------------------------
# 字幕設定の更新
# ------------------------------------------------------------
def set_subtitle(**kwargs):
    config = kwargs.get('config', Config())
    config.SUBTITLE_FONT_SIZE = int(kwargs.get('size', config.SUBTITLE_FONT_SIZE))

    # 色設定（1人目と2人目）
    config.SUBTITLE_FONT_COLOR[0] = kwargs.get('color1', kwargs.get('color', config.SUBTITLE_FONT_COLOR[0]))
    config.SUBTITLE_FONT_STROKE_COLOR[0] = kwargs.get('stroke_color1', kwargs.get('stroke_color', config.SUBTITLE_FONT_STROKE_COLOR[0]))
    config.SUBTITLE_FONT_COLOR[1] = kwargs.get('color2', config.SUBTITLE_FONT_COLOR[1])
    config.SUBTITLE_FONT_STROKE_COLOR[1] = kwargs.get('stroke_color2', config.SUBTITLE_FONT_STROKE_COLOR[1])

    config.SUBTITLE_FONT_STROKE_WIDTH = int(kwargs.get('stroke_width', config.SUBTITLE_FONT_STROKE_WIDTH))
    print(f"[字幕設定更新] size={config.SUBTITLE_FONT_SIZE}, color={config.SUBTITLE_FONT_COLOR}, stroke={config.SUBTITLE_FONT_STROKE_COLOR}")


# ------------------------------------------------------------
# タイトル設定の更新
# ------------------------------------------------------------
def set_title(**kwargs):
    config = kwargs.get('config', Config())
    config.TITLE_FONT_SIZE = int(kwargs.get('size', config.TITLE_FONT_SIZE))
    config.TITLE_FONT_COLOR = kwargs.get('color', config.TITLE_FONT_COLOR)
    config.TITLE_FONT_STROKE_COLOR = kwargs.get('stroke_color', config.TITLE_FONT_STROKE_COLOR)
    config.TITLE_FONT_STROKE_WIDTH = int(kwargs.get('stroke_width', config.TITLE_FONT_STROKE_WIDTH))
    print(f"[タイトル設定更新] size={config.TITLE_FONT_SIZE}, color={config.TITLE_FONT_COLOR}")


# ------------------------------------------------------------
# トーク設定
# ------------------------------------------------------------
def set_talk(**kwargs):
    config = kwargs.get('config', Config())
    config.TALK_SPEED = float(kwargs.get('speed', config.TALK_SPEED))
    config.SILENCE_DURATION = float(kwargs.get('silence_duration', config.SILENCE_DURATION))
    config.SPEAKERS[0] = int(kwargs.get('talker1', config.SPEAKERS[0]))
    config.SPEAKERS[1] = int(kwargs.get('talker2', config.SPEAKERS[1]))

    print(f"[会話設定更新] speed={config.TALK_SPEED}, silence={config.SILENCE_DURATION}, speakers={config.SPEAKERS}")


# ------------------------------------------------------------
# 背景色設定
# ------------------------------------------------------------
def set_background(color, config):
    config.BACKGROUND_COLOR = ast.literal_eval(color)
    print(f"[背景色設定] color={config.BACKGROUND_COLOR}")
