import tkinter
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
    TITLE_FONT_STROKE_WIDTH = 3

    # 動画の設定
    TALK_SPEED = 1.2
    SILENCE_DURATION = 0.5  # 音声合成の間の無音時間（秒）
    SPEAKERS = [2,3]

class TextRedirector:
    def __init__(self, text_widget):
        self.text_widget = text_widget
        self.line_buffer = ""

    def write(self, message):
        self.text_widget.after(0, self._append, message)

    def _append(self, message):
        if message == '\r':
            return  # 単体の\rは無視（不要）

        if '\r' in message:
            # 行頭戻り制御：現在の行を削除して書き直す
            parts = message.split('\r')
            for i, part in enumerate(parts):
                if i == 0:
                    self.line_buffer = part
                else:
                    self._overwrite_line(part)
        else:
            self.text_widget.insert(tkinter.END, message)
            self.text_widget.see(tkinter.END)

    def _overwrite_line(self, new_text):
        # 最後の行を削除して新しいテキストで上書き
        self.text_widget.delete("end-2l", "end-1l")  # 1行前を削除
        self.text_widget.insert(tkinter.END, new_text + '\n')
        self.text_widget.see(tkinter.END)

    def flush(self):
        pass
