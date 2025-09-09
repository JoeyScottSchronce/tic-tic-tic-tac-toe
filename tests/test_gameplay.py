import time
import unittest
from tic_tic_tic_tac_toe.game_logic import GameBoard, Cross, Circle

def pause():
    time.sleep(2)

class TestTicTacToe(unittest.TestCase):

    def setUp(self):
        self.game = GameBoard()
        self.circle = Circle(self.game)
        self.cross = Cross(self.game)

    def test_turn_enforcement(self):
        self.circle.make_move(0, 0)
        pause()
        self.circle.make_move(1, 1)  # Should be rejected
        pause()
        self.assertEqual(self.game.board[1][1], None)
        self.assertEqual(self.game.current_turn, 'X')

    def test_win_detection(self):
        self.circle.make_move(0, 0)
        pause()
        self.cross.make_move(1, 0)
        pause()
        self.circle.make_move(0, 1)
        pause()
        self.cross.make_move(1, 1)
        pause()
        self.circle.make_move(0, 2)  # Circle wins
        pause()
        self.assertTrue(self.game.game_over)
        self.assertEqual(self.game.board[0], ['O', 'O', 'O'])

    def test_move_depreciation(self):
        self.circle.make_move(0, 0)
        pause()
        self.cross.make_move(2, 2)
        pause()
        self.circle.make_move(1, 1)
        pause()
        self.cross.make_move(2, 1)
        pause()
        self.circle.make_move(1, 2)
        pause()
        self.cross.make_move(1, 0)
        pause()
        self.circle.make_move(0, 2)  # Should remove (0,0)
        pause()
        self.assertEqual(self.game.board[0][0], None)
        self.assertEqual(len(self.game.moves['O']), 3)

    def test_game_over_blocks_moves(self):
        self.circle.make_move(0, 0)
        pause()
        self.cross.make_move(1, 0)
        pause()
        self.circle.make_move(0, 1)
        pause()
        self.cross.make_move(1, 1)
        pause()
        self.circle.make_move(0, 2)  # Circle wins
        pause()
        self.cross.make_move(2, 2)   # Should be blocked
        pause()
        self.assertEqual(self.game.board[2][2], None)

    def test_reset_functionality(self):
        self.circle.make_move(0, 0)
        pause()
        self.cross.make_move(1, 1)
        pause()
        self.game.reset()
        pause()
        self.assertFalse(self.game.game_over)
        self.assertEqual(self.game.board, [[None]*3 for _ in range(3)])
        self.assertEqual(self.game.moves['O'], [])
        self.assertEqual(self.game.moves['X'], [])
        self.assertIsNone(self.game.current_turn)

    def test_no_depreciation_after_win(self):
        self.circle.make_move(0, 0)
        pause()
        self.cross.make_move(1, 0)
        pause()
        self.circle.make_move(0, 1)
        pause()
        self.cross.make_move(1, 1)
        pause()
        self.circle.make_move(0, 2)  # Circle wins
        pause()
        self.circle.make_move(2, 2)  # Should be blocked
        pause()
        self.assertEqual(len(self.game.moves['O']), 3)
        self.assertEqual(self.game.board[2][2], None)


if __name__ == '__main__':
    unittest.main()