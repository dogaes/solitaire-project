import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from game_logic import GameLogic

def test_start_game():
    game = GameLogic()
    game.start_new_game(7, "English")

    assert game.board.size == 7

def test_valid_move():

    game = GameLogic()
    game.start_new_game()

    game.board.board[3][1] == 0
    game.board.board[3][2] == 0
    game.board.board[3][3] == 1

    result = game.make_move((3, 3), (3, 5))

    assert result == True