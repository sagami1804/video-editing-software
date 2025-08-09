import re
from edit import *
from subtitle import *
from moviepy import *
from __init__ import *

# ------------------------------------------------------------
# テキスト解析・動画クリップ生成
# ------------------------------------------------------------
def analyze_text(full_text, is_talk_mode, is_green_mode):
    clips, images, bgm_time_stamps, bgms = [], [], [], []
    config = Config()
    current_time = 0.0
    talker = 0

    for line in map(str.strip, full_text.splitlines()):
        if not line:
            # 空行で話者を切り替え（トークモード時のみ）
            if is_talk_mode:
                talker = (talker + 1) % 2
            continue

        if line.startswith('\\'):
            result = handle_command_line(
                line, config, current_time, talker, clips, images, bgm_time_stamps, bgms
            )
            if result is None:
                return None
            current_time, talker = result
        else:
            # 通常のテキスト行（字幕クリップ）
            clip = make_subtitle_clip(line, talker, config).with_start(current_time)
            if clip is None:
                return None
            clips.append({"clip": clip, "z": 5})
            current_time += clip.duration

    # 背景設定
    background_color = config.BACKGROUND_COLOR if is_green_mode else (0, 255, 0)
    background_opacity = 1 if is_green_mode else 0
    background = ColorClip(size=(1920, 1080), color=background_color)\
        .with_duration(current_time)\
        .with_opacity(background_opacity)

    # z-index順にソートして合成
    sorted_clips = [item["clip"] for item in sorted(clips, key=lambda x: x["z"])]
    final = CompositeVideoClip([background] + sorted_clips, size=(1920, 1080))\
        .with_duration(current_time)
    return final

# ------------------------------------------------------------
# コマンド行の処理
# ------------------------------------------------------------
def handle_command_line(line, config, current_time, talker, clips, images, bgm_time_stamps, bgms):
    match = re.match(r'\\(\w+)(?:\{(.*)\})?', line)
    if not match:
        print(f"エラー：不明なコマンドです_{line}")
        return None

    command, raw_arg = match.group(1), match.group(2) or ""
    kwargs = parse_kwargs(raw_arg, config)

    if command == 'title':
        return handle_clip_command(title, kwargs, current_time, clips, z=1, talker=talker)

    elif command == 'se':
        return handle_clip_command(se, kwargs, current_time, clips, z=0, talker=talker)

    elif command == 'delay':
        current_time += float(kwargs['arg'])

    elif command == 'setBG':
        set_background(kwargs['arg'], config)

    elif command in ('setSubtitle', 'setTitle', 'setTalk'):
        handler_map = {
            'setSubtitle': set_subtitle,
            'setTitle': set_title,
            'setTalk': set_talk
        }
        if not isinstance(kwargs, dict):
            print(f"エラー:{command}の引数が不正です_{line}")
            return None
        handler_map[command](**kwargs)

    elif command == 'begin':
        return handle_begin_env(line, config, current_time, images, bgm_time_stamps, bgms, talker)

    elif command == 'end':
        return handle_end_env(line, current_time, images, clips, bgm_time_stamps, bgms, talker)

    else:
        print(f"エラー：不明なコマンドです_{line}")
        return None

    return current_time, talker

# ------------------------------------------------------------
# タイトルやSEのクリップ生成
# ------------------------------------------------------------
def handle_clip_command(func, kwargs, current_time, clips, z, talker):
    if not isinstance(kwargs, dict):
        print("エラー: 引数が不正です。辞書形式で渡してください。")
        return None
    clip = func(**kwargs).with_start(current_time)
    if clip is None:
        return None
    clips.append({"clip": clip, "z": z})
    return current_time + clip.duration, talker  # talker を維持して返す

# ------------------------------------------------------------
# \begin 環境の処理
# ------------------------------------------------------------
def handle_begin_env(line, config, current_time, images, bgm_time_stamps, bgms, talker):
    match = re.match(r"\\begin\{(\w+)\}(?:\[(.*?)\])?", line)
    if not match:
        print(f"エラー：不明なコマンドです_{line}")
        return None
    env_name, arg = match.group(1), match.group(2)
    if env_name == 'image':
        new_image = parse_kwargs(arg, config)
        new_image['start_time'] = current_time
        images.append(new_image)
    elif env_name == 'bgm':
        bgm_time_stamps.append(current_time)
        bgms.append(parse_kwargs(arg, config))
    else:
        print(f"エラー：不明な環境です_{line}")
        return None
    return current_time, talker

# ------------------------------------------------------------
# \end 環境の処理
# ------------------------------------------------------------
def handle_end_env(line, current_time, images, clips, bgm_time_stamps, bgms, talker):
    match = re.match(r"\\end\{(\w+)\}(?:\[(.*?)\])?", line)
    if not match:
        print(f"エラー：不明なコマンドです_{line}")
        return None

    env_name, arg = match.group(1), match.group(2)
    if env_name == 'image':
        if arg:
            clip, z, idx = serch_image(arg, images, current_time)
            if clip is None:
                return None
            images.pop(idx)
            clips.append({"clip": clip, "z": int(z)})
        else:
            last_image = images[-1]
            clip = image(current_time, last_image['start_time'], last_image['path'])
            if clip is None:
                return None
            clips.append({"clip": clip, "z": int(last_image.get('z', 0))})

    elif env_name == 'bgm':
        clip = bgm(current_time, bgm_time_stamps[-1], bgms[-1])
        if clip is None:
            return None
        clips.append({"clip": clip, "z": 0})

    else:
        print(f"エラー：不明な環境です_{line}")
        return None

    return current_time, talker

# ------------------------------------------------------------
# 引数文字列を辞書に変換
# ------------------------------------------------------------
def parse_kwargs(arg_str, config):
    if not arg_str:
        return {}
    if '=' not in arg_str:
        return {'arg': arg_str.strip()}
    kwargs = {k.strip(): v.strip() for k, v in (part.split('=', 1) for part in arg_str.split(','))}
    kwargs['config'] = config
    return kwargs

# ------------------------------------------------------------
# 指定タグの画像を検索してクリップ生成
# ------------------------------------------------------------
def serch_image(arg, images, current_time):
    tag = arg.split('=', 1)[1]
    for index, img in enumerate(images):
        if img.get('tag') == tag:
            clip = image(current_time, img['start_time'], img['path'])
            return clip, img.get('z', 0), index
    return None, 0, -1
