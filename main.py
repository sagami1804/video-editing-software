import multiprocessing
from gui import Editor

def main():
    multiprocessing.set_start_method("spawn", force=True)
    # GUIアプリケーションの初期化
    app = Editor()
    print("Starting GUI application...")
    
    #メインループ
    app.mainloop()
    
if __name__ == "__main__":
    main()