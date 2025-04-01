# main.py
import tkinter as tk
from chess_gui import ChessBoard

if __name__ == "__main__":
    print("Starting Chess Game...")
    root = tk.Tk()
    root.geometry("800x600+100+100")
    root.update()
    print("Tkinter root created with size 800x600 at position 100,100.")
    app = ChessBoard(root)
    print("ChessBoard initialized.")
    root.deiconify()
    root.lift()
    root.focus_force()
    root.attributes("-topmost", True)
    print("Window forced to top and focused.")
    print("Entering main loop...")
    root.mainloop()
    print("Main loop exited.")