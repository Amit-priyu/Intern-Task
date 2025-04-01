# Chess Game with Gemini AI

This project is a chess game built with Python and Tkinter, where we play as White, and the Gemini AI (via Google's Gemini API) plays as Black. The game features a graphical chessboard, piece movement, and AI integration for an interactive experience.

## Features
- Play chess against Gemini AI (Black).
- Graphical user interface (GUI) built with Tkinter.
- Move validation using the `python-chess` library.
- Gemini API integration to suggest moves for Black.
- **Fallback mechanism**: If Gemini fails to provide a valid move, a random legal move is selected for Black.

## Prerequisites
- **Python 3.9+**: Ensure Python is installed on your system.
- **Tkinter**: Comes with Python, but ensure it’s working:
  ```sh
  python3 -c "import tkinter; print(tkinter.TkVersion)"
  ```
- **Dependencies**:
  - `google-generativeai`: For Gemini API integration.
  - `python-chess`: For chess logic and move validation.
  - `pillow`: For loading chess piece images.
- **Gemini API Key**: Obtain a key from [Google AI Studio](https://aistudio.google.com/).

## Project Structure
```
chess_game/
├── main.py              # Entry point of the application
├── chess_gui.py         # GUI setup and rendering (chessboard and controls)
├── chess_logic.py       # Chess game logic (move validation, board state)
├── llm_engines.py       # Gemini AI integration for move suggestions
├── assets/              # Folder containing chess piece images
│   ├── white_p.png
│   ├── white_r.png
│   ├── white_n.png
│   ├── white_b.png
│   ├── white_q.png
│   ├── white_k.png
│   ├── black_p.png
│   ├── black_r.png
│   ├── black_n.png
│   ├── black_b.png
│   ├── black_q.png
│   ├── black_k.png
└── README.md            # Project documentation
```

## Setup Instructions

### 1. Clone or Create the Project
If cloning from a repository:
```sh
git clone <repository-url>
cd chess_game
```
Otherwise, create the folder structure as shown above and add the files.

### 2. Install Dependencies
Install the required Python packages:
```sh
pip3 install google-generativeai python-chess pillow
```

### 3. Add Chess Piece Images
- Download chess piece images (e.g., from Wikimedia Commons or Lichess GitHub).
- Use the **"cburnett" set** for compatibility.
- Rename the images to match the expected format (e.g., `white_p.png` for white pawn, `black_k.png` for black king).
- Place them in the `assets/` folder.

### 4. Obtain a Gemini API Key
1. Go to [Google AI Studio](https://aistudio.google.com/).
2. Sign in with your Google account.
3. Click **"Get API Key"** and create a new key.
4. Copy the key and keep it secure (you’ll need it to run the app).

## Running the Application

### Navigate to the Project Directory:
```sh
cd ~/path/to/chess_game
```

### Run the App:
```sh
python3 main.py
```

### Enter the Gemini API Key:
1. In the GUI, paste your **Gemini API key** into the text field labeled **"Gemini API Key:"**.
2. Click **"Set API Key"**. The status label should update to **"Gemini API Key Set Successfully"**, and the button will disable.

### Play the Game:
- You play as **White**. Click a white piece (e.g., a pawn at `e2`) and then a destination (e.g., `e4`) to move.
- Gemini (playing as **Black**) will respond with a move after a **500ms delay**.
- If Gemini fails to provide a valid move, a **random legal move** will be selected for Black.

## Troubleshooting

### GUI Doesn’t Appear:
- Ensure Tkinter is installed:
  ```sh
  python3 -c "import tkinter; print(tkinter.TkVersion)"
  ```
- Reinstall Python with Tkinter support:
  ```sh
  brew install python-tk@3.11
  ```
- Run with the specific Python version:
  ```sh
  /usr/local/bin/python3.11 main.py
  ```
### "No valid move from Gemini":
Check the **Terminal** for:
- **Gemini’s response**: `Gemini raw response: '...'`
- **Legal moves**: `Legal moves: [...]`

Possible issues:
- **Invalid Response**: Gemini might not return a UCI move (e.g., `e7e5`). The app attempts to parse common formats (e.g., `e5`), but if it fails, it falls back to a random move.
- **API Error**: Check for `Gemini Error: ...` in the Terminal (e.g., rate limit, invalid key, network issue).

### Missing Images:
Ensure all **12 images** are in `assets/` with the correct names. Missing images will result in **blank squares**, but the app will still run.

## Notes
- **Gemini API Limits**: The free tier allows **60 requests per minute** as of April 2025. If you hit the rate limit, **wait a minute and retry**.
- **Move Validation**: The app uses `python-chess` to ensure all moves (yours and Gemini’s) are **legal**.
- **Fallback Mechanism**: If Gemini fails to provide a valid move, the app selects a **random legal move** for Black to keep the game going.



## License
This project is for intern task.