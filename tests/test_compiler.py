import re
from test_edit import *
from test_subtitle import *
from moviepy import *

def analyze_text(full_text):
    analyzed_list = []

    text_line = full_text.splitlines()
    clips = []

    for line in text_line:
        line = line.strip()
        if not line:
            continue

        if line.startswith('\\'):
            analyzed_list.append({'type': 'command', 'text': line})

            # 正規表現でコマンド名と引数を抽出
            match = re.match(r'\\(\w+)(?:\{(.*)\})?', line)
            if match:
                command = match.group(1)
                raw_arg = match.group(2) if match.group(2) else ""
                print(f"コマンド名: {command}, 引数: {raw_arg}")

                # 引数文字列を辞書に変換
                kwargs = parse_kwargs(raw_arg)

                # コマンド名で関数呼び出し
                if command == 'section':
                    if isinstance(kwargs, dict):
                        section(**kwargs)
                    else:
                        section(kwargs)
                elif command == 'delay':
                    if isinstance(kwargs, dict):
                        delay(**kwargs)
                    else:
                        delay(kwargs)
                elif command == 'image':
                    if isinstance(kwargs, dict):
                        image(**kwargs)
                    else:
                        image(kwargs)
                elif command == 'setSubtitleScale':
                    if isinstance(kwargs, dict):
                        set_subtitle_scale(**kwargs)
                    else:
                        set_subtitle_scale(float(kwargs)) 
                elif command == 'setTalkSpeed':
                    if isinstance(kwargs, dict):
                        set_talk_speed(**kwargs)
                    else:
                        set_talk_speed(float(kwargs)) 
                
        else:
            analyzed_list.append({'type': 'text', 'text': line})
            print(clips)
            # テキストクリップの作成
            clips.append(make_subtitle_clip(line))
    
    # クリップを結合
    valid_clips = [clip for clip in clips if clip is not None]
    clip = concatenate_videoclips(valid_clips, method="compose")
    print("クリップが結合されました。")

    return clip

def parse_kwargs(arg_str):
    # 空なら空辞書
    if not arg_str:
        return {}

    # キー=値がない → 単一引数とみなす（位置引数として返す）
    if '=' not in arg_str:
        return arg_str.strip()

    # キー=値のときは辞書にする
    kwargs = {}
    for part in arg_str.split(','):
        if '=' in part:
            key, value = part.split('=', 1)
            kwargs[key.strip()] = value.strip()
    return kwargs


def set_subtitle_scale(scale=1.0):
    print(f"字幕のスケールを設定: {scale}")
    # 実際の処理はここに実装

def set_talk_speed(speed=1.0):
    print(f"話すスピードを設定: {speed}")
    # 実際の処理はここに実装
