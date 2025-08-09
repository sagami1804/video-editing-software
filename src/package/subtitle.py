import requests
from moviepy import TextClip, AudioFileClip, AudioClip, concatenate_audioclips
import re
import os
from __init__ import *


def make_subtitle_clip(text: str, talker: str, config):
    """
    テキストに対応する字幕付き動画クリップを作成する。

    Args:
        text (str): 字幕テキスト
        talker (str): 話者名（config.SPEAKERSのキー）
        config: 設定オブジェクト（フォントや速度などを含む）

    Returns:
        VideoClip: 字幕と音声が結合された動画クリップ
    """
    # 音声クリップを作成
    voice_clip = make_voice_clip(
        text, 
        speaker=config.SPEAKERS[talker], 
        speed=config.TALK_SPEED, 
        silence_duration=config.SILENCE_DURATION
    )
    clip_duration = voice_clip.duration

    # 字幕テキストクリップを作成
    subtitle_clip = TextClip(
        text=text,
        font=config.SUBTITLE_FONT,
        font_size=config.SUBTITLE_FONT_SIZE,
        color=config.SUBTITLE_FONT_COLOR[talker],
        stroke_color=config.SUBTITLE_FONT_STROKE_COLOR[talker],
        stroke_width=config.SUBTITLE_FONT_STROKE_WIDTH,
        size=(1700, 300),
        method='caption'
    ).with_position(('center', 'bottom')).with_duration(clip_duration)

    # 字幕クリップに音声を付加
    video_clip = subtitle_clip.with_audio(voice_clip)

    return video_clip


def make_voice_clip(text: str, speaker: int = 1, speed: float = 1.0, silence_duration: float = 1.0) -> AudioClip | None:
    """
    音声合成APIを使って音声クリップを生成し、無音クリップを付加して返す。

    Args:
        text (str): 合成するテキスト
        speaker (int): 話者ID
        speed (float): 話速倍率
        silence_duration (float): 音声後に付加する無音の長さ（秒）

    Returns:
        AudioClip | None: 合成した音声クリップ（無音付き）または失敗時はNone
    """
    # ファイル名に使えない文字を置換
    safe_filename = re.sub(r'[\\/*?:"<>|]', "_", text)
    filepath = f"data/temp_data/voice_{safe_filename}_{speed}_{speaker}.wav"

    if not os.path.exists(filepath):
        # 音声合成用クエリ作成
        query_payload = {'text': text, 'speaker': speaker}
        query_response = requests.post(
            'http://localhost:50021/audio_query',
            params=query_payload
        )
        if query_response.status_code != 200:
            print(f"Error in audio_query: {query_response.text}")
            return None

        query = query_response.json()
        query["speedScale"] = speed  # 話速を設定

        # 音声合成リクエスト
        synthesis_payload = {'speaker': speaker}
        synthesis_response = requests.post(
            'http://localhost:50021/synthesis',
            params=synthesis_payload,
            json=query
        )
        if synthesis_response.status_code != 200:
            print(f"Error in synthesis: {synthesis_response.text}")
            return None

        # 音声ファイル保存
        with open(filepath, 'wb') as f:
            f.write(synthesis_response.content)
        print(f"音声が {filepath} に保存されました。")

    # 音声クリップ読み込み
    audio_clip = AudioFileClip(filepath)
    # 無音クリップ作成
    silence_clip = AudioClip(lambda t: 0, duration=silence_duration, fps=44100)
    # 音声と無音を連結
    combined_clip = concatenate_audioclips([audio_clip, silence_clip])

    return combined_clip
