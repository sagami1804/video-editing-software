import tkinter
#　設定を保存するクラス
class Config:
    # 字幕の設定
    SUBTITLE_FONT = "fonts/Corporate-Logo-Rounded-Bold-ver3.otf"
    SUBTITLE_FONT_SIZE = 35
    SUBTITLE_FONT_COLOR = 'white'
    SUBTITLE_FONT_STROKE_COLOR = 'black'
    SUBTITLE_FONT_STROKE_WIDTH = 2

    # タイトルの設定
    TITLE_FONT = "fonts/Corporate-Logo-Rounded-Bold-ver3.otf"
    TITLE_FONT_SIZE = 100
    TITLE_FONT_COLOR = 'white'
    TITLE_FONT_STROKE_COLOR = 'black'
    TITLE_FONT_STROKE_WIDTH = 3

    # 動画の設定
    TALK_SPEED = 1.2
    SILENCE_DURATION = 0.5  # 音声合成の間の無音時間（秒）
    SPERKERS = [2,3]

class TextRedirector:
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, message):
        self.text_widget.after(0, self._append, message)

    def _append(self, message):
        self.text_widget.insert(tkinter.END, message)
        self.text_widget.see(tkinter.END)  # スクロール追従

    def flush(self):
        pass  # 必須：print()内部でflushされるため
