"""
Kivy UI for Tic-Tac-Toe game with game logic integration.
Displays a 3x3 grid, handles moves, turn switching, and win messages.
Grid lines and buttons are styled for appearance.
"""
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from game_logic import GameBoard, Circle, Cross


class Board(GridLayout):
    """
    Kivy widget for the tic-tac-toe board.
    Handles button layout, drawing grid lines, and connecting UI to game logic.
    """
    def __init__(self, status_label, **kwargs):
        """
        Initialize the board UI and game logic.
        Args:
            status_label (Label): Label widget to display game status.
            **kwargs: Additional GridLayout arguments.
        """
        super().__init__(**kwargs)
        self.cols = 3
        self.rows = 3
        self.size_hint = (None, None)
        self.size = (500, 500)
        self.padding = 10
        self.spacing = 10

    # Draw white tic-tac-toe grid behind buttons
        from kivy.graphics import Color, Line
        with self.canvas.before:
            Color(1, 1, 1, 1)
            self.v_lines = [Line(width=6) for _ in range(2)]
            self.h_lines = [Line(width=6) for _ in range(2)]
        self.bind(pos=self.update_lines, size=self.update_lines)

        # Game logic
        self.game = GameBoard()
        self.players = {'O': Circle(self.game), 'X': Cross(self.game)}
        self.status_label = status_label
        self.buttons = []
        # Create 3x3 grid of buttons
        for row in range(3):
            for col in range(3):
                btn = Button(
                    text='',
                    size_hint=(1, 1),
                    background_color=(1, 1, 1, 0),
                    background_normal='',
                    font_size=96
                )
                btn.bind(on_release=lambda btn, r=row, c=col: self.handle_move(r, c))
                self.buttons.append(btn)
                self.add_widget(btn)

    def handle_move(self, row, col):
        """
        Handles a button press for a move.
        Only allows moves for the current player, updates board and status.
        Args:
            row (int): Row index (0–2).
            col (int): Column index (0–2).
        """
        if self.game.game_over:
            self.status_label.text = "Press reset to play again."
            return
        current = self.game.current_turn
        # If no turn set, allow either player to start
        if current is None:
            current = 'X' if self.players['X'].symbol == 'X' else 'O'
        # Only allow move for current player
        if self.game.current_turn is not None and self.game.current_turn != self.players[current].symbol:
            self.status_label.text = f"It's {self.game.current_turn}'s turn."
            return
        player = self.players[current]
        player.make_move(row, col)
        self.update_board()
        if self.game.game_over:
            winner = self.game.current_turn if self.game.current_turn else player.symbol
            self.status_label.text = f"Game over! {winner} wins!"
        else:
            self.status_label.text = f"{self.game.current_turn}'s turn" if self.game.current_turn else "Next move!"

    def update_board(self):
        """
        Updates button text to reflect the current board state.
        """
        for i, btn in enumerate(self.buttons):
            row, col = divmod(i, 3)
            value = self.game.board[row][col]
            btn.text = value if value else ''

    def update_lines(self, *args):
        """
        Updates the position and size of grid lines when the board is resized or moved.
        """
        w, h = self.size
        x, y = self.pos
        cell_w = w / 3
        cell_h = h / 3
        for i in range(2):
            xpos = x + cell_w * (i + 1)
            self.v_lines[i].points = [xpos, y, xpos, y + h]
        for i in range(2):
            ypos = y + cell_h * (i + 1)
            self.h_lines[i].points = [x, ypos, x + w, ypos]

    def update_lines(self, *args):
        # Calculate positions for lines
        w, h = self.size
        x, y = self.pos
        cell_w = w / 3
        cell_h = h / 3
        # Vertical lines
        for i in range(2):
            xpos = x + cell_w * (i + 1)
            self.v_lines[i].points = [xpos, y, xpos, y + h]
        # Horizontal lines
        for i in range(2):
            ypos = y + cell_h * (i + 1)
            self.h_lines[i].points = [x, ypos, x + w, ypos]


class TicTacToeApp(App):
    """
    Main Kivy App for Tic-Tac-Toe.
    Sets up the layout, board, status label, and spacer.
    """
    def build(self):
        """
        Builds the main UI layout for the app.
        Returns:
            BoxLayout: The root widget containing all UI elements.
        """
        root = BoxLayout(orientation='vertical')
        status_label = Label(text="X's turn", size_hint=(1, 0.1), font_size=32)
        board = Board(status_label)
        board.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        root.add_widget(status_label)
        root.add_widget(board)
        root.add_widget(Widget(size_hint=(1, 0.1)))  # Spacer below the grid

        return root

if __name__ == '__main__':
    TicTacToeApp().run()
