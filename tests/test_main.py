from test_gui import *
from test_subtitle import *
import tkinter

def main():
    root = tkinter.Tk()
    app = Editor(root)
    print("Starting GUI application...")
    root.mainloop()
    
if __name__ == "__main__":
    main()