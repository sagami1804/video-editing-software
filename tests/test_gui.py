import tkinter
from tkinter import scrolledtext
from tkinter import filedialog
from test_compiler import *
import threading
import sys

class Editor(tkinter.Frame):
    def __init__(self, root):
        super().__init__()
        
        self.root = root
        self.root.title("エディタ")
        self.file_path = None
        
        #menuの作成
        self.menu = tkinter.Menu(self.root)
        self.root.config(menu=self.menu)
        self.file_menu = tkinter.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="ファイル", menu=self.file_menu)
        self.file_menu.add_command(label="新規", command=lambda: self.text_entry.delete("1.0", tkinter.END))
        self.file_menu.add_command(label="上書き保存", command=self.save_file)
        self.file_menu.add_command(label="別名で保存", command=self.save_file_dialog)
        self.file_menu.add_command(label="開く", command=self.open_file_dialog)
        
        # コードエディタ ラベル
        self.text_entry_label = tkinter.Label(root, text="コードエディタ", anchor="w")
        self.text_entry_label.grid(row=0, column=0, padx=10, pady=(7, 2), sticky="nw")

        # コードエディタ本体
        self.text_entry = scrolledtext.ScrolledText(self.root, font=("Consolas", 12), undo=True)
        self.text_entry.grid(row=1, column=0, rowspan=2, sticky="nsew", padx=10, pady=(0, 10))

        # 実行ログ ラベル
        self.log_label = tkinter.Label(root, text="実行ログ", anchor="w")
        self.log_label.grid(row=3, column=0, padx=10, pady=(7, 2), sticky="nw")
        
        # 実行ログ出力エリア
        self.log_output = scrolledtext.ScrolledText(self.root, font=("Consolas", 10), height=10, state="normal")
        self.log_output.grid(row=4, column=0, columnspan=2, sticky="nsew", padx=10, pady=(0, 10))
        
        # ボタンの作成
        self.button_frame = tkinter.Frame(root,relief="solid", bd=1)
        self.button_frame.grid(row=2, column=1, sticky="e", padx=10, pady=10) 
        self.preview_button = tkinter.Button(self.button_frame, text="コンパイル", width=10, command=self.run_execution)
        self.preview_button.grid(row=0, column=0, sticky="e", padx=10, pady=10) 
        self.preview_button = tkinter.Button(self.button_frame, text="プレビュー", width=10, command=self.run_execution)
        self.preview_button.grid(row=1, column=0, sticky="e", padx=10, pady=10) 
        self.output_button = tkinter.Button(self.button_frame, text="出力", width=10, command=self.run_execution)
        self.output_button.grid(row=2, column=0, sticky="e", padx=10, pady=10) 

        # 標準出力と標準エラー出力をリダイレクト
        sys.stdout = TextRedirector(self.log_output)
        sys.stderr = TextRedirector(self.log_output)
        
        # ウィンドウのリサイズに追従させる
        self.root.grid_rowconfigure(1, weight=1)  # エディタ部分の行
        self.root.grid_rowconfigure(3, weight=0)  # ログ出力の行（必要なら weight=1 にしても可）
        self.root.grid_columnconfigure(0, weight=1)  # エディタ部分の列
        self.root.grid_columnconfigure(1, weight=0)  # ボタン部分の列
    
    def run_compile(self):
        threading.Thread(target=self.execution, daemon=True).start()
        
    def run_preview(self):
        threading.Thread(target=self.execution, daemon=True).start()
        
    def run_execution(self):
        threading.Thread(target=self.execution, daemon=True).start()
        
    def compile_clip(self):
        print("コンパイルを開始します")
        clip = analyze_text(self.text_entry.get("1.0", tkinter.END))
        print("コンパイルが正常に完了しました")
        return clip
        
    def preview(self):
        clip = self.compile_clip()
        print("プレビューを表示します(音ズレは仕様です)")
        clip.preview(fps=2,audio_fps=11000,audio_buffersize=1000)  # プレビュー表示
            
    # 実行ボタンがクリックされたときの処理
    def execution(self):
        clip = self.compile_clip()
        clip = clip.with_fps(24)  # フレームレートを設定

        # 動画クリップの書き出し
        print("動画クリップの書き出しを開始します...")
        clip.write_videofile(
            "output/output.mp4",
            codec="h264_nvenc",        # ← GPU対応コーデック
            audio_codec="aac",
            threads=8,
            bitrate="5M",
            ffmpeg_params=[
                "-preset", "fast",     # 高速設定（slow～fastまで選べる）
                "-rc", "vbr",          # 可変ビットレート（cbr固定も可）
            ],
        )
        print("動画ファイルが出力されました")
    
    # ファイルを開く
    def open_file_dialog(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if self.file_path:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                self.text_entry.delete("1.0", tkinter.END)
                self.text_entry.insert(tkinter.END, content)
    
    # ファイルを別名で保存する
    def save_file_dialog(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            with open(file_path, 'w', encoding='utf-8') as file:
                content = self.text_entry.get("1.0", tkinter.END)
                file.write(content)
    
    # 上書き保存
    def save_file(self):
        current_text = self.text_entry.get("1.0", tkinter.END)
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
    root = tkinter.Tk()
    app = Editor(root)
    root.mainloop()
