# tic-tic-tic-tac-toe

A modern version of Tic Tac Toe where ties are impossible! The game continues until a winner is declared, thanks to move depreciation—oldest moves disappear, keeping the board dynamic.

## Features

- **Kivy UI:** Responsive, modern interface with a 3x3 grid, styled buttons, and clear status messages.
- **Endless Play:** No ties—moves depreciate, so the game always ends with a win.
- **Strict Game Logic:** Turn enforcement, win detection, and move depreciation are all handled in `game_logic.py`.
- **Reset Functionality:** Instantly restart the game with a button.
- **Color Customization:** X and O symbols are color-coded for clarity.
- **Modular Structure:** All code is organized in a package for easy maintenance and deployment.
- **Unit Tests:** Core game logic is covered by tests in the `tests/` directory.

## Folder Structure

```
tic-tic-tic-tac-toe/
│
├── main.py                  # Entry point for the Kivy app
├── requirements.txt         # All dependencies for the project
├── README.md                # This file
├── tic_tic_tic_tac_toe/     # Main package
│   ├── __init__.py
│   ├── game_logic.py        # Game rules, board, player logic
│   └── ui.py                # Kivy UI and app class
├── tests/                   # Unit tests
│   ├── test_cases.py        # Game logic tests
│   ├── test_gameplay.py     # Additional gameplay tests
│   └── __pycache__/
├── .venv/                   # Python virtual environment
├── __pycache__/
```

## Setup

1. **Clone the repository** and navigate to the project folder.
2. **Create a virtual environment** (recommended):
   ```pwsh
   python -m venv .venv
   ```
3. **Activate the virtual environment**:
   - PowerShell: `./.venv/Scripts/Activate`
   - CMD: `./.venv/Scripts/activate.bat`
   - Bash: `source .venv/bin/activate`
4. **Install dependencies**:
   ```pwsh
   pip install -r requirements.txt
   ```

## Running the App

```pwsh
python main.py
```
This launches the Kivy UI. Play by clicking the grid buttons. Use the reset button to restart.

## Running Tests

```pwsh
python -m unittest discover tests
```
This runs all unit tests for the game logic.

## Linting & Formatting

- Recommended: Use `flake8` for linting and `black` for formatting.
- To lint:
  ```pwsh
  pip install flake8
  flake8 tic_tic_tic_tac_toe tests
  ```
- To format:
  ```pwsh
  pip install black
  black tic_tic_tic_tac_toe tests
  ```

## Notes

- If you add new dependencies, update `requirements.txt` with `pip freeze > requirements.txt`.
