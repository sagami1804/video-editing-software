import requests
from moviepy import *
import re

font = "fonts/Corporate-Logo-Rounded-Bold-ver3.otf"
font_size = 24
subtitle_color = 'white'
subtitle_stroke_color = 'black'

def make_subtitle_clip(text):
    # 音声合成の関数を呼び出して音声クリップを作成
    voice_clip = make_voice_clip(text)
    clip_duration = voice_clip.duration
    
    # テキストクリップを作成
    subtitle_clip = TextClip(text=text, font=font, font_size=font_size, color=subtitle_color, stroke_color=subtitle_stroke_color, stroke_width=3, size=(1700, 100), method='caption')
    subtitle_clip = subtitle_clip.with_position(('center', 'bottom')).with_duration(clip_duration)
    video_clip = CompositeVideoClip([subtitle_clip])
    video_clip = video_clip.with_audio(voice_clip)
    
# 音声合成の関数
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

text = "こんにちは、今日は「国境」に隠された不思議について、ちょっと深掘りしていきましょう。"
make_subtitle_clip(text)
        