import customtkinter as ctk
from tkinter import filedialog, messagebox
from compiler import analyze_text
import threading
import sys
from multiprocessing import Process
import signal
import os


class TextRedirector:
    def __init__(self, text_widget):
        self.text_widget = text_widget
        self.line_buffer = ""

    def write(self, message):
        self.text_widget.after(0, self._append, message)

    def _append(self, message):
        if message == '\r':
            return  # 単体の\rは無視

        if '\r' in message:
            parts = message.split('\r')
            for i, part in enumerate(parts):
                if i == 0:
                    self.line_buffer = part
                else:
                    self._overwrite_line(part)
        else:
            self.text_widget.configure(state="normal")
            self.text_widget.insert("end", message)
            self.text_widget.see("end")
            self.text_widget.configure(state="disabled")

    def _overwrite_line(self, new_text):
        self.text_widget.configure(state="normal")
        # 最後の行を削除（1行分）して上書き
        self.text_widget.delete("end-2l", "end-1l")
        self.text_widget.insert("end", new_text + '\n')
        self.text_widget.see("end")
        self.text_widget.configure(state="disabled")

    def flush(self):
        pass


def preview_worker(text, talk_mode, is_green_mode):
    """動画プレビューを別プロセスで実行するワーカ関数"""
    clip = analyze_text(text, talk_mode, is_green_mode)
    if clip is None:
        return
    clip = clip.resized((896, 504)).with_fps(3)
    try:
        clip.preview(fps=3, audio_fps=11100)
    except OSError:
        os.kill(os.getpid(), signal.SIGTERM)


class Editor(ctk.CTk):
    WINDOW_TITLE = "モダンエディタ"
    WINDOW_SIZE = "1000x800"
    FONT_MAIN = ("Meiryo", 11, "bold")
    FONT_CODE = ("Consolas", 14)
    FONT_LOG = ("Meiryo", 10)

    def __init__(self):
        super().__init__()
        self.title(self.WINDOW_TITLE)
        self.geometry(self.WINDOW_SIZE)
        self.file_path = None
        self.preview_proc = None  # プレビュー用プロセス保持

        self._setup_appearance()
        self._setup_layout()
        self._redirect_stdout()

    def _setup_appearance(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

    def _setup_layout(self):
        # メインのグリッド設定
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=5)
        self.grid_rowconfigure(2, weight=1)

        self._create_top_menu()
        self._create_center_text_area()
        self._create_button_panel()
        self._create_log_area()

    def _create_top_menu(self):
        top_frame = ctk.CTkFrame(self, corner_radius=0)
        top_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=5)

        ctk.CTkButton(top_frame, text="新規", font=self.FONT_MAIN, command=self.new_text).pack(side="left", padx=5)
        ctk.CTkButton(top_frame, text="開く", font=self.FONT_MAIN, command=self.open_file_dialog).pack(side="left", padx=5)
        ctk.CTkButton(top_frame, text="保存", font=self.FONT_MAIN, command=self.save_file).pack(side="left", padx=5)
        ctk.CTkButton(top_frame, text="別名保存", font=self.FONT_MAIN, command=self.save_file_dialog).pack(side="left", padx=5)

        self.is_talk_mode = ctk.BooleanVar(value=False)
        self.is_green_mode = ctk.BooleanVar(value=False)

        ctk.CTkCheckBox(top_frame, text="会話モード", variable=self.is_talk_mode).pack(side="right", padx=10)
        ctk.CTkCheckBox(top_frame, text="グリーンバックモード", variable=self.is_green_mode).pack(side="right", padx=10)

    def _create_center_text_area(self):
        center_frame = ctk.CTkFrame(self, corner_radius=0)
        center_frame.grid(row=1, column=0, rowspan=3, sticky="nsew", padx=10, pady=5)
        center_frame.grid_rowconfigure(0, weight=5)
        center_frame.grid_columnconfigure(0, weight=1)

        self.text_entry = ctk.CTkTextbox(
            center_frame,
            font=self.FONT_CODE,
            wrap="none",
            border_width=1,
            corner_radius=0,
        )
        self.text_entry.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

    def _create_button_panel(self):
        button_frame = ctk.CTkFrame(self, corner_radius=0)
        button_frame.grid(row=1, column=1, sticky="ns", padx=10, pady=5)

        ctk.CTkButton(button_frame, text="コンパイル", font=self.FONT_MAIN, command=self.run_compile).pack(pady=5)
        ctk.CTkButton(button_frame, text="プレビュー", font=self.FONT_MAIN, command=self.run_preview).pack(pady=5)
        ctk.CTkButton(button_frame, text="プレビュー停止", font=self.FONT_MAIN, command=self.stop_preview).pack(pady=5)
        ctk.CTkButton(button_frame, text="出力", font=self.FONT_MAIN, command=self.run_execution).pack(pady=5)

    def _create_log_area(self):
        log_frame = ctk.CTkFrame(self, corner_radius=0)
        log_frame.grid(row=4, column=0, columnspan=2, sticky="nsew", padx=10, pady=5)
        log_frame.grid_rowconfigure(0, weight=1)
        log_frame.grid_columnconfigure(0, weight=1)

        self.log_output = ctk.CTkTextbox(
            log_frame,
            font=self.FONT_LOG,
            border_width=1,
            corner_radius=0,
            state="disabled",
        )
        self.log_output.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

    def _redirect_stdout(self):
        sys.stdout = TextRedirector(self.log_output)
        sys.stderr = TextRedirector(self.log_output)

    # --- ファイル操作関連 ---
    def new_text(self):
        """テキストエリアをクリアして新規作成"""
        if messagebox.askyesno('確認', '今のデータはすべて削除されます。新規作成しますか？'):
            self.text_entry.delete("1.0", "end")
            self.file_path = None
            print("新規作成しました。")
        else:
            print("新規作成をキャンセルしました。")

    def open_file_dialog(self):
        """ファイルを開いてテキストを読み込む"""
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            self.file_path = file_path
            self._load_file(file_path)

    def _load_file(self, path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            self.text_entry.delete("1.0", "end")
            self.text_entry.insert("end", content)
            print(f"ファイルを読み込みました: {path}")
        except Exception as e:
            print(f"ファイル読み込みエラー: {e}")

    def save_file_dialog(self):
        """別名で保存ダイアログを表示"""
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            self.file_path = file_path
            self._save_file(file_path)

    def save_file(self):
        """現在のファイルパスに上書き保存"""
        if not self.file_path:
            self.save_file_dialog()
            return

        current_text = self.text_entry.get("1.0", "end").strip()
        if current_text:
            self._save_file(self.file_path)
        else:
            print("保存する内容がありません。")

    def _save_file(self, path):
        try:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(self.text_entry.get("1.0", "end"))
            print(f"ファイルが保存されました: {path}")
        except Exception as e:
            print(f"ファイル保存エラー: {e}")

    # --- コンパイル・プレビュー・出力関連 ---
    def run_compile(self):
        threading.Thread(target=self.compile_clip, daemon=True).start()

    def compile_clip(self):
        """テキストを解析して動画クリップを生成"""
        print("コンパイルを開始します")
        clip = analyze_text(self.text_entry.get("1.0", "end"), self.is_talk_mode.get(), self.is_green_mode.get())
        if clip is None:
            print("コンパイルが失敗しました")
            return None
        print("コンパイルが正常に完了しました")
        return clip

    def run_preview(self):
        """プレビューを別プロセスで開始"""
        if getattr(self, "preview_proc", None) and self.preview_proc.is_alive():
            print("既にプレビュー中です。")
            return

        text = self.text_entry.get("1.0", "end")
        talk_mode = self.is_talk_mode.get()
        green_mode = self.is_green_mode.get()

        # プロセスが残っていたらクリーンアップ
        if getattr(self, "preview_proc", None):
            try:
                self.preview_proc.join(timeout=0.1)
            except Exception:
                pass

        print("プレビューを開始しています...(音ズレは仕様です)")
        self.preview_proc = Process(target=preview_worker, args=(text, talk_mode, green_mode))
        self.preview_proc.start()

    def stop_preview(self):
        """プレビュー用プロセスを停止"""
        proc = getattr(self, "preview_proc", None)
        if proc and proc.is_alive():
            print("プレビューを停止します")
            try:
                proc.terminate()
                proc.join(timeout=1)
            except Exception as e:
                print(f"停止時に例外: {repr(e)}")
            finally:
                self.preview_proc = None
        else:
            print("プレビューは実行中ではありません")

    def run_execution(self):
        threading.Thread(target=self.execution, daemon=True).start()

    def execution(self):
        clip = self.compile_clip()
        if clip is None:
            return
        clip = clip.with_fps(24)

        print("動画クリップの書き出しを開始します...")
        try:
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
        except Exception as e:
            print(f"動画書き出し中にエラーが発生しました: {e}")


if __name__ == "__main__":
    app = Editor()
    app.mainloop()
