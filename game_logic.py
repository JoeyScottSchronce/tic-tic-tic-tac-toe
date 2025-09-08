class GameBoard:
    """
    Represents the state and rules of a 3x3 Tic Tac Toe board with move depreciation.
    Attributes:
        board (list[list[Optional[str]]]): 3x3 grid storing 'X', 'O', or None.
        moves (dict[str, list[tuple[int, int]]]): Tracks each player's move history.
        game_over (bool): Flag indicating if the game has ended.
        current_turn (Optional[str]): Tracks whose turn it is ('X' or 'O').
    """

    def __init__(self):
        """Initializes an empty board and resets game state."""
        self.board = [[None for _ in range(3)] for _ in range(3)]
        self.moves = {'O': [], 'X': []}
        self.game_over = False
        self.current_turn = None

    def display(self):
        """Prints the current board state in a human-readable format."""
        for row in self.board:
            print([cell if cell else ' ' for cell in row])
        print()

    def reset(self):
        """
        Resets the board and game state to start a new game.
        Clears all moves, resets turn tracking, and prints the empty board.
        """
        self.board = [[None for _ in range(3)] for _ in range(3)]
        self.moves = {'O': [], 'X': []}
        self.game_over = False
        self.current_turn = None
        print("Game has been reset. Let's play again!")
        print(f"{self.current_turn} starts the game!\n")
        self.display()

    def check_winner(self, symbol):
        """
        Checks if the given symbol ('X' or 'O') has a winning line.
        Args:
            symbol (str): The player's symbol to check.
        Returns:
            bool: True if the player has won, False otherwise.
        """
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
    Attributes:
        symbol (str): The player's symbol ('X' or 'O').
        board (GameBoard): Reference to the shared game board.
    """

    def __init__(self, symbol, board: GameBoard):
        """
        Initializes a player with a symbol and links to the game board.
        Args:
            symbol (str): 'X' or 'O'.
            board (GameBoard): The shared game board instance.
        """
        self.symbol = symbol
        self.board = board

    def make_move(self, row, col):
        """
        Attempts to place the player's symbol at the given position.
        Enforces turn order, prevents overwriting, checks for win condition,
        and depreciates oldest move if more than 3 are active.
        Args:
            row (int): Row index (0–2).
            col (int): Column index (0–2).
        """
        if self.board.game_over:
            print(f"Game is over. {self.symbol} cannot move.")
            return

        # Initialize turn on first move
        if self.board.current_turn is None:
            self.board.current_turn = self.symbol
            print(f"{self.symbol} starts the game!\n")

        if self.board.current_turn != self.symbol:
            print(f"It's not {self.symbol}'s turn.")
            return

        if self.board.board[row][col] is not None:
            print(f"{self.symbol} tried ({row},{col}) but it's taken.")
            return

        # Place symbol and record move
        self.board.board[row][col] = self.symbol
        self.board.moves[self.symbol].append((row, col))
        print(f"{self.symbol} placed at ({row},{col})")

        # Check win before depreciation
        if self.board.check_winner(self.symbol):
            self.board.display()
            print(f"{self.symbol} wins!")
            self.board.game_over = True
            return

        # Depreciate oldest move if more than 3
        if len(self.board.moves[self.symbol]) > 3:
            old_row, old_col = self.board.moves[self.symbol].pop(0)
            self.board.board[old_row][old_col] = None
            print(f"{self.symbol}'s move at ({old_row},{old_col}) was removed")

        # Switch turn
        self.board.current_turn = 'X' if self.symbol == 'O' else 'O'
        self.board.display()


class Circle(Play):
    """
    Represents the 'O' player.
    """
    def __init__(self, board):
        super().__init__('O', board)


class Cross(Play):
    """
    Represents the 'X' player.
    """
    def __init__(self, board):
        super().__init__('X', board)
