import re
from test_edit import *
from test_subtitle import *
from moviepy import *
from __init__ import *

def analyze_text(full_text, is_talk_mode):
    analyzed_list = []  # 解析結果を格納するリスト
    clips = []  # 動画クリップを格納するリスト
    image_time_stamps = []    # 画像のタイムスタンプを格納するリスト
    images = [] # 画像のパスを格納するリスト[{path, z-index, tag, current_time},{path, z-index, tag, current_time}]
    bgm_time_stamps = []  # BGMのタイムスタンプを格納するリスト
    bgms = []  # BGMのパスを格納するリスト
    config = Config()  # 設定を初期化
    current_time = 0.0  # 現在の動画時間を初期化
    talker = 0
    
    text_line = full_text.splitlines() # テキストを行単位で分割
    for line in text_line:
        # 行の前後の空白を削除
        line = line.strip() 
        if not line:
            if is_talk_mode:
                talker = (talker+1) % 2
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
                    clips.append({"clip": clip, "z": 1})  # タイトルクリップを追加
                    current_time += clip.duration   # 現在の動画時間を更新
                
                elif command == 'image':
                    if isinstance(kwargs, dict):
                        clip = image_overlay(**kwargs) 
                        if clip:
                            z_index = int(kwargs.get('z', 1))

                            clips.append({"clip": clip.with_start(current_time), "z": z_index})
                

                # SEクリップの生成
                elif command == 'se':
                    if isinstance(kwargs, dict):
                        clip = se(**kwargs).with_start(current_time)  # SEクリップの生成
                        clips.append({"clip": clip, "z": 0})  # SEクリップを追加
                    else:
                        print("seの引数が不正です。辞書形式で渡してください。")
                    
                elif command == 'delay':    # 遅延時間の追加
                    current_time += float(kwargs['arg'])
                    
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
                        new_image = parse_kwargs(arg,config)
                        new_image['start_time'] = current_time  # 開始時間を記録
                        images.append(new_image)  # 画像のパスを記録
                    elif env_name == 'bgm':
                        bgm_time_stamps.append(current_time)  # BGMの開始時間を記録
                        bgms.append(parse_kwargs(arg,config))  # BGMのオプションを記録
                        
                elif command == 'end':  # 環境の終了
                    match = re.match(r"\\end\{(\w+)\}(?:\[(.*?)\])?", line)
                    if match:
                        env_name = match.group(1)  # {}の中身
                        arg = match.group(2)       # []の中身（なければ None）
                        if env_name == 'image':  # 画像クリップの終了
                            if arg:  # 引数がある場合
                                clips_array = serch_image(arg, images, current_time)  # 画像のパスを検索
                                clip = clips_array[0]  # 画像クリップを取得
                                z = clips_array[1]  # z-indexを取得
                                images.pop(clips_array[2])  # 使用済みの画像を削除
                                clips.append({"clip": clip, "z": int(z)})  # 画像クリップを追加
                            else:
                                clip = image(current_time, images[-1]['start_time'], images[-1]['path'])  # 画像クリップを生成
                                clips.append({"clip": clip, "z": int(images[-1].get('z',0))}) 
                            
                        elif env_name == 'bgm':  # BGMの終了
                            clip = bgm(current_time, bgm_time_stamps[-1], bgms[-1])  # BGMクリップを生成
                            clips.append({"clip": clip, "z": 0}) 
                            
        else:   # テキスト行の処理
            clip = make_subtitle_clip(line, talker, config).with_start(current_time) # 字幕クリップの生成
            clips.append({"clip": clip, "z": 2})  # 字幕クリップを追加
            current_time += clip.duration   # 現在の動画時間を更新
    
    # クリップを結合
    clips = [item["clip"] for item in sorted(clips, key=lambda x: x["z"])]  # z値でソート
    background = ColorClip(size=(1920, 1080), color=(0, 255, 0)).with_duration(current_time).with_opacity(0)    # 背景クリップを生成
    final = CompositeVideoClip([background] + clips, size=(1920, 1080)).with_duration(current_time) # すべてのクリップを合成
    return final

# 引数文字列を辞書に変換する関数
def parse_kwargs(arg_str,config):
    # 空なら空辞書
    if not arg_str:
        return {}

    kwargs = {}
    # キー=値がない → 単一引数とみなす（位置引数として返す）
    if '=' not in arg_str:
        kwargs['arg'] = arg_str.strip()
        return kwargs
    

    # キー=値のときは辞書にする
    for part in arg_str.split(','):
        if '=' in part:
            key, value = part.split('=', 1)
            kwargs[key.strip()] = value.strip()
    
    # 辞書に設定を含める   
    kwargs['config'] = config 
    return kwargs


def serch_image(arg, images, current_time):
    print(f"画像検索: 引数='{arg}', 現在の時間={current_time}")
    tag = arg.split('=', 1)[1]
    for index, img in enumerate(images):
        if 'tag' in img and img['tag'] == tag:
            clip = image(current_time, img['start_time'], img['path'])
            z = img.get('z', 0)  # z-indexを取得
            return clip, z, index
    return None, 0, -1
