import tkinter
from tkinter import scrolledtext

class Editor(tkinter.Frame):
    def __init__(self, root):
        super().__init__()
        
        self.root = root
        self.root.title("エディタ")
        
        #menuの作成
        self.menu = tkinter.Menu(self.root)
        self.root.config(menu=self.menu)
        self.file_menu = tkinter.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="ファイル", menu=self.file_menu)
        self.file_menu.add_command(label="新規", command=lambda: self.text_entry.delete("1.0", tkinter.END))
        self.file_menu.add_command(label="保存", command=lambda: print("保存機能は未実装です。"))
        self.file_menu.add_separator()
        self.file_menu.add_command(label="終了", command=self.root.quit)
        
        # スクロール可能なテキストエリアの作成
        self.text_entry = scrolledtext.ScrolledText(self.root)
        self.text_entry.grid(row=0, column=0, sticky="nsew")  # スクロール可能なテキストエリア
        
        # ボタンの作成
        self.button = tkinter.Button(self.root, text="実行", width=10, command=self.execution)
        self.button.grid(row=0, column=1, sticky="e") 
        
        # ウィンドウのリサイズに追従させる
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
    
    # 実行ボタンがクリックされたときの処理
    def execution(self):
        
        text_content = self.text_entry.get("1.0", tkinter.END)
        print("実行ボタンがクリックされました。テキスト内容:")
        print(text_content)
        
if __name__ == "__main__":
    root = tkinter.Tk()
    app = Editor(root)
    root.mainloop()
