import re
from moviepy import *
#画像クリップを生成
def image(current_time, start_time, path):
    img_clip = ImageClip(path).with_duration(current_time - start_time).with_start(start_time)
    img_clip = img_clip.with_position(('center', 'center'))
    return img_clip
    
#セクションタイトル（テロップ）を生成
def section(**kwargs):
    text = kwargs.get('text', ' ')
    duration = float(kwargs.get('duration', 3))
    clip = TextClip(text=text, font_size=100, color='white', font="fonts/Corporate-Logo-Rounded-Bold-ver3.otf", size=(1700, 300)).with_duration(duration)
    clip = clip.with_position(('center', 'center'))
    return clip

#無音の「音声クリップ」を生成
def delay(**kwargs):
    duration = float(kwargs.get('duration', 1))
    clip = TextClip(text="", font_size=70, color='white', font="fonts/Corporate-Logo-Rounded-Bold-ver3.otf", size=(1700, 300)).with_duration(duration)
    video_clip = CompositeVideoClip([clip])
    audio_clip = AudioClip(lambda t: 0, duration=duration, fps=44100)
    video_clip = video_clip.with_audio(audio_clip)
    return video_clip