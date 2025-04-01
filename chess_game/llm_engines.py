# llm_engines.py
import google.generativeai as genai
import chess

print("Loading llm_engines.py...")

class LLMoveGenerator:
    def __init__(self, gui):
        print("Initializing LLMoveGenerator...")
        self.gui = gui
        self.gemini_api_key = None
        self.is_key_set = False

    def set_keys(self):
        if self.is_key_set:
            print("Gemini API key already set, skipping...")
            return
        
        print("Setting Gemini API key...")
        self.gemini_api_key = self.gui.gemini_key_entry.get()
        
        if self.gemini_api_key:
            try:
                genai.configure(api_key=self.gemini_api_key)
                self.gui.status_label.config(text="Gemini API Key Set Successfully")
                self.is_key_set = True
                self.gui.set_key_button.config(state="disabled")
                print("Gemini API key set successfully.")
            except Exception as e:
                self.gui.status_label.config(text=f"Error setting Gemini key: {e}")
                print(f"Error setting Gemini key: {e}")
        else:
            self.gui.status_label.config(text="Please enter a valid Gemini API Key")
            print("No Gemini API key entered.")

    def get_gemini_move(self):
        print("Requesting move from Gemini...")
        if not self.gemini_api_key:
            self.gui.status_label.config(text="Gemini API Key not set!")
            print("Gemini API key not set.")
            return None
        
        try:
            fen = self.gui.logic.board.fen()
            prompt = (
                f"Chess position (FEN): {fen}. You are playing as {'white' if self.gui.logic.turn == 'white' else 'black'}. "
                f"Suggest the best move in UCI format (e.g., 'e2e4'). Do not include any additional text, explanations, or moves in other formats. "
                f"Only return the UCI move."
            )
            print(f"Prompt sent to Gemini: {prompt}")
            
            # Uncomment the following line to test with a mock response
            # move_str = "e7e5"  # Mock response for testing
            # print("Using mock response: 'e7e5'")
            
            # Comment out the API call when testing with mock response
            model = genai.GenerativeModel('gemini-pro')
            response = model.generate_content(prompt)
            move_str = response.text.strip()
            print(f"Gemini raw response: '{move_str}'")

            # Try to parse the response as a UCI move
            if len(move_str) == 4 and move_str.isalnum():
                # Direct UCI format (e.g., 'e7e5')
                pass
            else:
                # Fallback: Try to parse common formats like "e5" or "pawn to e5"
                move_str = move_str.lower()
                if " to " in move_str:
                    # Example: "pawn to e5" -> "e5"
                    move_str = move_str.split(" to ")[-1].strip()
                if len(move_str) == 2:  # Example: "e5"
                    # Convert to UCI (e.g., "e5" -> "e7e5" for a pawn)
                    piece_type = chess.PAWN
                    to_square = chess.parse_square(move_str)
                    for move in self.gui.logic.board.legal_moves:
                        if move.to_square == to_square and self.gui.logic.board.piece_at(move.from_square).piece_type == piece_type:
                            move_str = move.uci()
                            break
                    else:
                        print(f"Could not convert '{move_str}' to a valid UCI move.")
                        return None

            # Validate the move
            legal_moves = [m.uci() for m in self.gui.logic.board.legal_moves]
            print(f"Legal moves: {legal_moves}")
            if move_str in legal_moves:
                move = chess.Move.from_uci(move_str)
                print(f"Valid move found: {move_str}")
                return move
            else:
                print(f"Move '{move_str}' is not legal. Legal moves are: {legal_moves}")
                # Fallback: Select a random legal move if Gemini fails
                if legal_moves:
                    import random
                    move_str = random.choice(legal_moves)
                    print(f"Fallback: Using random legal move: {move_str}")
                    return chess.Move.from_uci(move_str)
                return None
        except Exception as e:
            self.gui.status_label.config(text=f"Gemini Error: {str(e)}")
            print(f"Gemini Error: {str(e)}")
            # Fallback on API error: Select a random legal move
            legal_moves = [m.uci() for m in self.gui.logic.board.legal_moves]
            if legal_moves:
                import random
                move_str = random.choice(legal_moves)
                print(f"Fallback on API error: Using random legal move: {move_str}")
                return chess.Move.from_uci(move_str)
            return None

    def ai_move(self, gui):
        print("AI move requested...")
        if not gui.logic.board.is_game_over():
            move = self.get_gemini_move()
            if move and move in gui.logic.board.legal_moves:
                gui.logic.board.push(move)
                gui.update_board()
                gui.logic.turn = "white"
                gui.turn_label.config(text="White's Turn")
                print(f"AI moved: {move.uci()}")
            else:
                self.gui.status_label.config(text="No valid move from Gemini")
                print("No valid move returned from Gemini.")