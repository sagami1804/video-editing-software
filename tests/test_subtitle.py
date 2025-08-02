import requests
from moviepy import *
import re


# 字幕クリップの作成
def make_subtitle_clip(text):
    subtitle_font = "fonts/Corporate-Logo-Rounded-Bold-ver3.otf"
    subtitle_font_size = 24
    subtitle_color = 'white'
    subtitle_stroke_color = 'black'
    subtitle_stroke_width = 2

    # 音声合成の関数を呼び出して音声クリップを作成
    voice_clip = make_voice_clip(text)
    clip_duration = voice_clip.duration
    
    # テキストクリップを作成
    subtitle_clip = TextClip(text=text, font=subtitle_font, font_size=subtitle_font_size, color=subtitle_color, stroke_color=subtitle_stroke_color, subtitle_stroke_width=3, size=(1700, 100), method='caption')
    subtitle_clip = subtitle_clip.with_position(('center', 'bottom')).with_duration(clip_duration)
    video_clip = CompositeVideoClip([subtitle_clip])
    video_clip = video_clip.with_audio(voice_clip)
    
# 音声合成
def make_voice_clip(text, speaker=1, speed=1):
    filename = re.sub(r'[\\/*?:"<>|]', "_", text)
    filepath = f"data/temp_data/voice_{filename}.wav"
    
    
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
    audio_clip = AudioFileClip(filepath)
    
    return audio_clip

        