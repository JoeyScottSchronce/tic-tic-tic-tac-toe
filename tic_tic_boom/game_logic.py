"""
game_logic.py

Core logic for Tic Tac Toe with move depreciation.
Includes board state management, turn enforcement, and win detection.
Designed for integration with a Kivy UI or other front-end.
"""

class GameBoard:
    """
    Represents the state and rules of a 3x3 Tic Tac Toe board with move depreciation.
    """

    def __init__(self):
        self.board = [[None for _ in range(3)] for _ in range(3)]
        self.moves = {"O": [], "X": []}
        self.game_over = False
        self.current_turn = None

    def reset(self):
        self.board = [[None for _ in range(3)] for _ in range(3)]
        self.moves = {"O": [], "X": []}
        self.game_over = False
        self.current_turn = None

    def check_winner(self, symbol: str) -> bool:
        b = self.board

        # Check rows
        for row in b:
            if all(cell == symbol for cell in row):
                return True

        # Check columns
        for col in range(3):
            if all(b[row][col] == symbol for row in range(3)):
                return True

        # Check diagonals
        if all(b[i][i] == symbol for i in range(3)):
            return True
        if all(b[i][2 - i] == symbol for i in range(3)):
            return True

        return False


class Play:
    """
    Represents a player and encapsulates move logic, turn enforcement, and depreciation.
    """

    def __init__(self, symbol: str, board: GameBoard):
        self.symbol = symbol
        self.board = board

    def make_move(self, row: int, col: int):
        if self.board.game_over:
            return

        if self.board.current_turn is None:
            self.board.current_turn = self.symbol

        if self.board.current_turn != self.symbol:
            return

        if self.board.board[row][col] is not None:
            return

        # Place symbol and record move
        self.board.board[row][col] = self.symbol
        self.board.moves[self.symbol].append((row, col))

        # Depreciate oldest move if more than 3
        if len(self.board.moves[self.symbol]) > 3:
            old_row, old_col = self.board.moves[self.symbol].pop(0)
            self.board.board[old_row][old_col] = None

        # Check win after depreciation
        if self.board.check_winner(self.symbol):
            self.board.game_over = True
            return

        # Switch turn
        self.board.current_turn = "X" if self.symbol == "O" else "O"


class Circle(Play):
    """Represents the 'O' player."""
    def __init__(self, board: GameBoard):
        super().__init__("O", board)


class Cross(Play):
    """Represents the 'X' player."""
    def __init__(self, board: GameBoard):
        super().__init__("X", board)
