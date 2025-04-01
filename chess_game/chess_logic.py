# chess_logic.py
import chess

print("Loading chess_logic.py...")

class ChessLogic:
    def __init__(self):
        print("Initializing ChessLogic...")
        self.board = chess.Board()
        self.turn = "white"
        self.selected_piece = None
        self.last_move = None

    def select_piece(self, pos, gui):
        print(f"Selecting piece at {pos}...")
        if self.selected_piece is None:
            piece = self.board.piece_at(chess.parse_square(pos))
            if piece and ((self.turn == "white" and piece.color == chess.WHITE) or (self.turn == "black" and piece.color == chess.BLACK)):
                self.selected_piece = pos
                gui.update_board()
                print(f"Piece selected at {pos}.")
        else:
            if self.selected_piece == pos:
                self.selected_piece = None
                gui.update_board()
                print("Selection cleared.")
                return
            move = chess.Move.from_uci(self.selected_piece + pos)
            if move in self.board.legal_moves:
                self.board.push(move)
                print(f"Move made: {self.selected_piece}{pos}")
                self.last_move = (self.selected_piece, pos)
                self.selected_piece = None
                gui.update_board()
                self.turn = "black" if self.turn == "white" else "white"
                gui.turn_label.config(text=("Black's Turn" if self.turn == "black" else "White's Turn"))
                gui.root.after(500, lambda: gui.llm.ai_move(gui))
            else:
                self.selected_piece = None
                gui.update_board()
                print("Invalid move attempted.")