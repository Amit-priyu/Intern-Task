# chess_gui.py
import tkinter as tk
from functools import partial
from pathlib import Path
from PIL import Image, ImageTk
import chess
from chess_logic import ChessLogic
from llm_engines import LLMoveGenerator

print("Loading chess_gui.py...")

class ChessBoard:
    def __init__(self, root):
        print("Initializing ChessBoard...")
        self.root = root
        self.root.title("Chess Game")
        self.root.configure(bg="gray20")

        self.logic = ChessLogic()
        self.llm = LLMoveGenerator(self)
        self.squares = {}
        self.piece_images = self.load_piece_images()
        print("Piece images loaded.")
        self.create_gui()
        print("GUI created.")

    def load_piece_images(self):
        print("Loading piece images...")
        images = {}
        base_path = Path(__file__).parent / "assets"
        for color in ["white", "black"]:
            for piece in ["p", "r", "n", "b", "q", "k"]:
                file_path = base_path / f"{color}_{piece}.png"
                try:
                    if file_path.exists():
                        img = Image.open(file_path).resize((80, 80))
                        images[f"{color}_{piece}"] = ImageTk.PhotoImage(img)
                    else:
                        print(f"Warning: {file_path} not found. Using blank image.")
                except Exception as e:
                    print(f"Error loading {file_path}: {e}")
        images["blank"] = ImageTk.PhotoImage(Image.new("RGBA", (80, 80), (255, 255, 255, 0)))
        return images

    def create_gui(self):
        print("Creating GUI elements...")
        self.main_frame = tk.Frame(self.root, bg="gray20")
        self.main_frame.pack()

        self.board_frame = tk.Frame(self.main_frame, bg="gray20", padx=10, pady=10)
        self.board_frame.grid(row=0, column=0)

        self.info_frame = tk.Frame(self.main_frame, bg="gray20")
        self.info_frame.grid(row=0, column=1, padx=20)

        self.turn_label = tk.Label(self.info_frame, text="White's Turn", font=("Arial", 16), fg="white", bg="gray20")
        self.turn_label.pack(pady=10)

        self.status_label = tk.Label(self.info_frame, text="Enter Gemini API Key to start", font=("Arial", 14, "bold"), fg="yellow", bg="gray20", wraplength=200, justify="center")
        self.status_label.pack(pady=10)

        self.api_key_label = tk.Label(self.info_frame, text="Gemini API Key:", font=("Arial", 12), fg="white", bg="gray20")
        self.api_key_label.pack(pady=5)

        self.gemini_key_entry = tk.Entry(self.info_frame, width=30)
        self.gemini_key_entry.pack(pady=2)

        self.set_key_button = tk.Button(self.info_frame, text="Set API Key", command=self.llm.set_keys)
        self.set_key_button.pack(pady=5)

        self.create_board()
        self.update_board()

    def create_board(self):
        print("Creating board squares...")
        for row in range(8):
            for col in range(8):
                square_color = "#8B4513" if (row + col) % 2 == 0 else "#F0D9B5"
                pos = f"{chr(97 + col)}{8 - row}"
                btn = tk.Button(
                    self.board_frame,
                    bg=square_color,
                    activebackground="goldenrod",
                    relief=tk.RAISED,
                    borderwidth=2,
                    image=self.piece_images["blank"],
                    width=80,
                    height=80,
                    compound="center",
                    command=partial(self.logic.select_piece, pos, self)  # Pass self as gui
                )
                btn.grid(row=row, column=col, padx=1, pady=1)
                self.squares[pos] = btn
        print("Board squares created.")

    def update_board(self):
        print("Updating board...")
        for pos, btn in self.squares.items():
            piece = self.logic.board.piece_at(chess.parse_square(pos))
            if piece:
                color = "white" if piece.color == chess.WHITE else "black"
                piece_key = f"{color}_{piece.symbol().lower()}"
                btn.config(image=self.piece_images.get(piece_key, self.piece_images["blank"]),
                          bg=("#8B4513" if (ord(pos[0]) + int(pos[1])) % 2 == 0 else "#F0D9B5"))
            else:
                btn.config(image=self.piece_images["blank"],
                          bg=("#8B4513" if (ord(pos[0]) + int(pos[1])) % 2 == 0 else "#F0D9B5"))
        print("Board updated.")