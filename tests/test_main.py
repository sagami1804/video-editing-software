from test_gui import *
from test_subtitle import *
import tkinter
import os

def main():
    # カレントディレクトリをvideo-editing-softwareに移動
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(script_dir)
    os.chdir(parent_dir)
    
    # GUIアプリケーションの初期化
    root = tkinter.Tk()
    app = Editor(root)
    print("Starting GUI application...")
    
    #メインループ
    root.mainloop()
    
if __name__ == "__main__":
    main()