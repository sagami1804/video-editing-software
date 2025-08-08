import re
from test_edit import *
from test_subtitle import *
from moviepy import *
from __init__ import *

def analyze_text(full_text):
    analyzed_list = []  # 解析結果を格納するリスト
    clips = []  # 動画クリップを格納するリスト
    image_time_stamps = []    # 画像のタイムスタンプを格納するリスト
    images = [] # 画像のパスを格納するリスト
    bgm_time_stamps = []  # BGMのタイムスタンプを格納するリスト
    bgms = []  # BGMのパスを格納するリスト
    config = Config()  # 設定を初期化
    current_time = 0.0  # 現在の動画時間を初期化
    
    text_line = full_text.splitlines() # テキストを行単位で分割
    for line in text_line:
        # 行の前後の空白を削除
        line = line.strip() 
        if not line:
            continue

        # コマンド行の処理
        if line.startswith('\\'):
            analyzed_list.append({'type': 'command', 'text': line})

            # 正規表現でコマンド名と引数を抽出
            match = re.match(r'\\(\w+)(?:\{(.*)\})?', line)
            if match:  
                command = match.group(1)
                raw_arg = match.group(2) if match.group(2) else ""
                print(f"コマンド名: {command}, 引数: {raw_arg}")

                # 引数文字列を辞書に変換
                kwargs = parse_kwargs(raw_arg,config)

                # コマンド名で関数呼び出し
                if command == 'title':  # タイトルクリップの生成
                    if isinstance(kwargs, dict):    # 辞書形式で引数が渡された場合
                        clip = title(**kwargs).with_start(current_time)
                    else:
                        print("titleの引数が不正です。辞書形式で渡してください。")
                    clips.append(clip)  # タイトルクリップを追加
                    current_time += clip.duration   # 現在の動画時間を更新
                
                # SEクリップの生成
                elif command == 'se':
                    if isinstance(kwargs, dict):
                        clip = se(**kwargs).with_start(current_time)  # SEクリップの生成
                        clips.append(clip)  # SEクリップを追加
                    else:
                        print("seの引数が不正です。辞書形式で渡してください。")
                    
                elif command == 'delay':    # 遅延時間の追加
                    current_time += float(kwargs)
                    
                elif command == 'setSubtitle':  # 字幕設定の更新
                    if isinstance(kwargs, dict):
                        set_subtitle(**kwargs)
                    else:
                        print("setSubtitleScaleの引数が不正です。辞書形式で渡してください。")
                        
                elif command == 'setTalk': # 話すスピードの設定
                    if isinstance(kwargs, dict):
                        set_talk(**kwargs)
                    else:
                        print("setTalkSpeedの引数が不正です。辞書形式で渡してください。")
                
                elif command == 'begin':    # 環境の開始
                    match = re.match(r"\\begin\{(\w+)\}(?:\[(.*?)\])?", line)
                    if match:
                        env_name = match.group(1)  # {}の中身
                        arg = match.group(2)       # []の中身（なければ None）
                    if env_name  == 'image':    # 画像クリップの開始
                        image_time_stamps.append(current_time)    #画像の開始時間を記録
                        images.append(arg)  # 画像のパスを記録
                    elif env_name == 'bgm':
                        bgm_time_stamps.append(current_time)  # BGMの開始時間を記録
                        bgms.append(parse_kwargs(arg,config))  # BGMのオプションを記録
                        
                elif command == 'end':  # 環境の終了
                    match = re.match(r"\\end\{(\w+)\}", line)
                    if match:
                        env_name = match.group(1)  # {}の中身
                        if env_name == 'image': # 画像クリップの終了
                            clip = image(current_time, image_time_stamps[-1], images[-1]) # 画像クリップを生成
                            clips.append(clip)
                        elif env_name == 'bgm':  # BGMの終了
                            clip = bgm(current_time, bgm_time_stamps[-1], bgms[-1])  # BGMクリップを生成
                            clips.append(clip)
                            
        else:   # テキスト行の処理
            clip = make_subtitle_clip(line,config).with_start(current_time) # 字幕クリップの生成
            clips.append(clip)  # 字幕クリップを追加
            current_time += clip.duration   # 現在の動画時間を更新
    
    # クリップを結合
    background = ColorClip(size=(1920, 1080), color=(0, 255, 0)).with_duration(current_time).with_opacity(0)    # 背景クリップを生成
    final = CompositeVideoClip([background] + clips, size=(1920, 1080)).with_duration(current_time) # すべてのクリップを合成
    return final

# 引数文字列を辞書に変換する関数
def parse_kwargs(arg_str,config):
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
    
    # 辞書に設定を含める   
    kwargs['config'] = config
    return kwargs



