import re
from moviepy import *

def image(**kwargs):
    path = kwargs.get('path')
    duration = float(kwargs.get('duration'))
    try:
        return ImageClip(path)
    except Exception as e:
        return None

def section(**kwargs):
    text = kwargs.get('text', ' ')
    duration = float(kwargs.get('duration', 3))

    return TextClip(text, fontsize=70, color='white', font='Arial-Bold').with_duratio(duration)

def delay(**kwargs):
    duration = float(kwargs.get('duration', 1))
    
    return AudioClip(lambda t: 0, duration=duration)