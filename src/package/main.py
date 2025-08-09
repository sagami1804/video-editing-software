from gui import Editor
import os

def main():
    # カレントディレクトリをvideo-editing-softwareに移動
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(os.path.dirname(script_dir))
    os.chdir(parent_dir)
    
    # GUIアプリケーションの初期化
    app = Editor()
    print("Starting GUI application...")
    
    #メインループ
    app.mainloop()
    
if __name__ == "__main__":
    main()