import customtkinter as ctk
from tkinter import filedialog, messagebox
from test_compiler import *
import threading
import sys
from multiprocessing import Process
import signal
import os

# 標準出力リダイレクト用クラス
class TextRedirector:
    def __init__(self, widget):
        self.widget = widget
    def write(self, text):
        self.widget.configure(state="normal")
        self.widget.insert("end", text)
        self.widget.see("end")
        self.widget.configure(state="disabled")
    def flush(self):
        pass

def preview_worker(text, talk_mode):
    clip = analyze_text(text, talk_mode).resized((1280, 720)).with_fps(3)
    try:
        clip.preview(fps=3, audio_fps=11100)
    except OSError:
        os.kill(os.getpid(), signal.SIGTERM)
        

class Editor(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("モダンエディタ")
        self.geometry("1000x800")
        self.file_path = None
        self.preview_proc = None  # プレビュー用スレッド保持

        # ダークモード設定
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        font_main = ("Meiryo", 11, "bold")

        # レイアウト設定
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=5)
        self.grid_rowconfigure(2, weight=1)

        # 上部メニュー的ボタン類のフレーム（角を鋭角に）
        top_frame = ctk.CTkFrame(self, corner_radius=0)
        top_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=5)

        ctk.CTkButton(top_frame, text="新規", font=font_main, command=self.new_text).pack(side="left", padx=5)
        ctk.CTkButton(top_frame, text="開く", font=font_main, command=self.open_file_dialog).pack(side="left", padx=5)
        ctk.CTkButton(top_frame, text="保存", font=font_main, command=self.save_file).pack(side="left", padx=5)
        ctk.CTkButton(top_frame, text="別名保存", font=font_main, command=self.save_file_dialog).pack(side="left", padx=5)

        self.is_talk_mode = ctk.BooleanVar(value=False)
        ctk.CTkCheckBox(top_frame, text="会話モード", variable=self.is_talk_mode).pack(side="right", padx=10)

        # 中央エリアのフレーム（角を鋭角に）
        center_frame = ctk.CTkFrame(self, corner_radius=0)
        center_frame.grid(row=1, column=0, rowspan=3, sticky="nsew", padx=10, pady=5)
        center_frame.grid_rowconfigure(0, weight=5)
        center_frame.grid_columnconfigure(0, weight=1)

        # テキストエリアも角を鋭角に設定
        self.text_entry = ctk.CTkTextbox(center_frame, font=("Consolas",14), wrap="none",
                                         border_width=1, corner_radius=0)
        self.text_entry.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        # ボタン列のフレーム（角を鋭角に）
        button_frame = ctk.CTkFrame(self, corner_radius=0)
        button_frame.grid(row=1, column=1, sticky="ns", padx=10, pady=5)

        ctk.CTkButton(button_frame, text="コンパイル", font=font_main, command=self.run_compile).pack(pady=5)
        ctk.CTkButton(button_frame, text="プレビュー", font=font_main, command=self.run_preview).pack(pady=5)
        ctk.CTkButton(button_frame, text="プレビュー停止", font=font_main, command=self.stop_preview).pack(pady=5)
        ctk.CTkButton(button_frame, text="出力", font=font_main, command=self.run_execution).pack(pady=5)

        # ログ出力エリアのフレーム（角を鋭角に）
        log_frame = ctk.CTkFrame(self, corner_radius=0)
        log_frame.grid(row=4, column=0, columnspan=2, sticky="nsew", padx=10, pady=5)
        log_frame.grid_rowconfigure(0, weight=1)
        log_frame.grid_columnconfigure(0, weight=1)

        # ログテキストエリアも角を鋭角に
        self.log_output = ctk.CTkTextbox(log_frame, font=("Meiryo", 10),
                                         border_width=1, corner_radius=0)
        self.log_output.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        sys.stdout = TextRedirector(self.log_output)
        sys.stderr = TextRedirector(self.log_output)
    
    def new_text(self):
        ref = messagebox.askyesno('確認', '今のデータはすべて削除されます。新規作成しますか？')
        if ref:
            self.text_entry.delete("1.0", "end")
            self.file_path = None
            print("新規作成しました。")
        else:
            print("新規作成をキャンセルしました。")

    def run_compile(self):
        threading.Thread(target=self.compile_clip, daemon=True).start()

    def run_preview(self):
        # preview_proc が生きているかどうかを安全に判定
        if getattr(self, "preview_proc", None) and self.preview_proc.is_alive():
            print("既にプレビュー中です。")
            return

        text_value = self.text_entry.get("1.0", "end")
        talk_mode_value = self.is_talk_mode.get()

        # multiprocessing の起動前に既にプロセスが残っている場合はクリーンアップ
        if getattr(self, "preview_proc", None):
            try:
                self.preview_proc.join(timeout=0.1)
            except Exception:
                pass

        # 子プロセスをトップレベル関数で起動（引数は文字列と bool のみ）
        print("プレビューを開始しています...(音ズレは仕様です)")
        self.preview_proc = Process(target=preview_worker, args=(text_value, talk_mode_value))
        self.preview_proc.start()
    
    def stop_preview(self):
        proc = getattr(self, "preview_proc", None)
        if proc and proc.is_alive():
            print("プレビューを停止します")
            try:
                proc.terminate()
                proc.join(timeout=1)
            except Exception as e:
                print("停止時に例外:", repr(e))
            finally:
                self.preview_proc = None
        else:
            print("プレビューは実行中ではありません")

    def run_execution(self):
        threading.Thread(target=self.execution, daemon=True).start()

    def compile_clip(self):
        print("コンパイルを開始します")
        clip = analyze_text(self.text_entry.get("1.0", "end"), self.is_talk_mode.get())
        print("コンパイルが正常に完了しました")
        return clip

    def execution(self):
        clip = self.compile_clip()
        clip = clip.with_fps(24)
        print("動画クリップの書き出しを開始します...")
        clip.write_videofile(
            "output/output.mp4",
            codec="h264_nvenc",
            audio_codec="aac",
            threads=8,
            bitrate="5M",
            ffmpeg_params=["-preset", "fast", "-rc", "vbr"],
        )
        messagebox.showinfo('メッセージ', '動画ファイルが出力されました')
        print("動画ファイルが出力されました")

    def open_file_dialog(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if self.file_path:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                self.text_entry.delete("1.0", "end")
                self.text_entry.insert("end", file.read())

    def save_file_dialog(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(self.text_entry.get("1.0", "end"))

    def save_file(self):
        current_text = self.text_entry.get("1.0", "end")
        if not self.file_path:
            self.save_file_dialog()
            return
        if current_text.strip():
            with open(self.file_path, 'w', encoding='utf-8') as file:
                file.write(current_text)
            print("ファイルが上書き保存されました。")
        else:
            print("保存する内容がありません。")
    
if __name__ == "__main__":
    app = Editor()
    app.mainloop()
