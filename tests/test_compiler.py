import re
from test_edit import *
from test_subtitle import *
from moviepy import *

def analyze_text(full_text):
    analyzed_list = []

    text_line = full_text.splitlines()
    clips = []
    time_stamps = []
    images = []
    current_time = 0.0
    '''
    txt_clip = TextClip(text="", font_size=70, color='white', font="fonts/Corporate-Logo-Rounded-Bold-ver3.otf", size=(1700, 300)).with_duration(1)
    audio_clip = AudioClip(lambda t: 0, duration=1, fps=44100)
    clip = txt_clip.with_audio(audio_clip)
    clips.append(clip)
    current_time += clip.duration
    '''
    
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
                        clip = section(**kwargs,start_time=current_time).with_start(current_time)
                    else:
                        clip = section(kwargs).with_start(current_time)
                    clips.append(clip)
                    current_time += clip.duration
                    
                elif command == 'delay':
                    current_time += 3  # 無音の長さを1秒と仮定
                    
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
                
                elif command == 'begin':
                    match = re.match(r"\\begin\{(\w+)\}(?:\[(.*?)\])?", line)

                    if match:
                        env_name = match.group(1)  # {}の中身
                        arg = match.group(2)       # []の中身（なければ None）
                    if env_name  == 'image':
                        time_stamps.append(current_time)
                        images.append(arg)
                        
                elif command == 'end':
                    match = re.match(r"\\end\{(\w+)\}", line)
                    if match:
                        env_name = match.group(1)  # {}の中身
                        if env_name == 'image':
                            clip = image(current_time, time_stamps[-1], images[-1])
                            clips.append(clip)
                            
        else:
            clip = make_subtitle_clip(line).with_start(current_time)
            clips.append(clip)
            current_time += clip.duration
        
        print(current_time)
    
    # クリップを結合
    background = ColorClip(size=(1920, 1080), color=(0, 255, 0)).with_duration(current_time).with_opacity(0)
    final = CompositeVideoClip([background] + clips, size=(1920, 1080)).with_duration(current_time)
    return final

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
