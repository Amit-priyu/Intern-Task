# test_tk.py
import tkinter as tk

print("Starting Tkinter test...")
root = tk.Tk()
root.title("Test Window")
root.geometry("300x200")  # Set a visible size
label = tk.Label(root, text="Hello, Tkinter!", font=("Arial", 20))
label.pack(pady=20)
print("Window created.")
root.mainloop()
print("Test complete.")