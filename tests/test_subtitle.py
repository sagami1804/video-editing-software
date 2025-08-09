import requests
from moviepy import *
import re
import os
from __init__ import *


# 字幕クリップの作成
def make_subtitle_clip(text, talker, config):
    # 音声合成の関数を呼び出して音声クリップを作成
    voice_clip = make_voice_clip(text, speaker=config.SPEAKERS[talker], speed=config.TALK_SPEED, silence_duration=config.SILENCE_DURATION)
    clip_duration = voice_clip.duration
    
    
    # テキストクリップを作成
    subtitle_clip = TextClip(text=text, font=config.SUBTITLE_FONT, font_size=config.SUBTITLE_FONT_SIZE, color=config.SUBTITLE_FONT_COLOR[talker], stroke_color=config.SUBTITLE_FONT_STROKE_COLOR[talker], stroke_width=config.SUBTITLE_FONT_STROKE_WIDTH, size=(1700, 300), method='caption')
    subtitle_clip = subtitle_clip.with_position(('center', 'bottom')).with_duration(clip_duration)
    video_clip = subtitle_clip.with_audio(voice_clip)
    
    return video_clip
    
# 音声合成
def make_voice_clip(text, speaker=1, speed=1, silence_duration=1):
    filename = re.sub(r'[\\/*?:"<>|]', "_", text)
    filepath = f"data/temp_data/voice_{filename}_{speed}_{speaker}.wav"
    
    if not os.path.exists(filepath): # ファイルが存在しない場合のみ音声合成を実行
        # 1. テキストから音声合成のためのクエリを作成
        query_payload = {'text': text, 'speaker': speaker}
        query_response = requests.post(f'http://localhost:50021/audio_query', params=query_payload)

        if query_response.status_code != 200:
            print(f"Error in audio_query: {query_response.text}")
            return

        query = query_response.json()
        #トークスピードを設定
        query["speedScale"] = speed

        # 2. クエリを元に音声データを生成
        synthesis_payload = {'speaker': speaker}
        synthesis_response = requests.post(f'http://localhost:50021/synthesis', params=synthesis_payload, json=query)

        if synthesis_response.status_code == 200:
            # 音声ファイルとして保存
            with open(filepath, 'wb') as f:
                f.write(synthesis_response.content)
            print(f"音声が {filepath} に保存されました。")
        else:
            print(f"Error in synthesis: {synthesis_response.text}")
            return
    
    # 音声クリップを作成
    audio_clips = []
    audio_clips.append(AudioFileClip(filepath)) # 音声ファイルを追加
    audio_clips.append(AudioClip(lambda t: 0, duration=silence_duration, fps=44100)) # 無音クリップを追加
    audio_clip = concatenate_audioclips(audio_clips) # クリップを結合
    return audio_clip

        