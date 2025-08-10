
#　設定を保存するクラス
class Config:
    # 字幕の設定
    SUBTITLE_FONT = "fonts/Corporate-Logo-Rounded-Bold-ver3.otf"
    SUBTITLE_FONT_SIZE = 35
    SUBTITLE_FONT_COLOR = ['white', 'white']
    SUBTITLE_FONT_STROKE_COLOR = ['#FF00BF', "#00CC1B"]
    SUBTITLE_FONT_STROKE_WIDTH = 4

    # タイトルの設定
    TITLE_FONT = "fonts/Corporate-Logo-Rounded-Bold-ver3.otf"
    TITLE_FONT_SIZE = 100
    TITLE_FONT_COLOR = 'white'
    TITLE_FONT_STROKE_COLOR = 'black'
    TITLE_FONT_STROKE_WIDTH = 6

    # 動画の設定
    TALK_SPEED = 1.1
    SILENCE_DURATION = 0.5  # 音声合成の間の無音時間（秒）
    SPEAKERS = [2,3]
    BACKGROUND_COLOR = (0,255,0)  # グリーンバックモードの背景色

