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
        
        # スクロール可能なテキストエリアの作成
        self.text_entry = scrolledtext.ScrolledText(self.root, font=("Arial", 12), undo=True)
        self.text_entry.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)  # スクロール可能なテキストエリア
        
        # ボタンの作成
        self.button = tkinter.Button(self.root, text="実行", width=10, command=self.run_execution)
        self.button.grid(row=0, column=1, sticky="e", padx=10, pady=10) 
        
        # 実行ログ出力エリア
        self.log_output = scrolledtext.ScrolledText(self.root, font=("Consolas", 10), height=10, state="normal")
        self.log_output.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=10, pady=(0, 10))

        # 標準出力と標準エラー出力をリダイレクト
        sys.stdout = TextRedirector(self.log_output)
        sys.stderr = TextRedirector(self.log_output)
        
        self.root.grid_rowconfigure(0, weight=3)  # テキスト入力
        self.root.grid_rowconfigure(1, weight=1)  # ログ出力
        self.root.grid_columnconfigure(0, weight=1)
        
        # ウィンドウのリサイズに追従させる
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
    
    def run_execution(self):
        threading.Thread(target=self.execution, daemon=True).start()
        
    # 実行ボタンがクリックされたときの処理
    def execution(self):
        text_content = self.text_entry.get("1.0", tkinter.END)
        print("実行ボタンがクリックされました。テキスト内容:")
        print(text_content)
        
        # テキスト内容を解析して動画クリップを生成
        print("テキスト内容を解析して動画クリップを生成します...")
        clip = analyze_text(text_content)
        
        # 動画クリップの書き出し
        print("動画クリップの書き出しを開始します...")
        clip = clip.resized((640, 360)).with_fps(2)  # 動画の解像度とフレームレートを設定
        clip.preview(fps=2,audio_fps=11000,audio_buffersize=1000)  # プレビュー表示
        clip.write_videofile(
            "output/output.mp4",
            codec="libx264",  # ← GPUエンコード
            audio_codec="aac",
            threads=10,  # スレッド数も指定可能
            bitrate="3M"
        )
    
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
