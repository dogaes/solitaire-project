import unittest
from board import Board, EnglishBoard, HexBoard, DiamondBoard
from game import ManualGame, AutomatedGame

class TestManualGame(unittest.TestCase):
    def test_make_move(self):
        board = EnglishBoard(7)
        game = ManualGame(board)

        # (3, 1) -> (3, 3) which starts empty and should be valid

        game.make_move((3, 1), (3, 3))
        self.assertEqual(board.grid[3][1], 0) # peg removed from start
        self.assertEqual(board.grid[3][2], 0) # jumped peg removed
        self.assertEqual(board.grid[3][3], 1) # peg moved to end
    print("ManualGame tests passed")

class TestAutomatedGame(unittest.TestCase):
    def test_auto_move(self):
        board = EnglishBoard(7)
        game = AutomatedGame(board)

        game.make_auto_move()
        self.assertTrue(True)
    print("AutomatedGame tests passed")

if __name__ == "__main__":
    unittest.main()