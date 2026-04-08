from abc import ABC, abstractmethod
import random
from board import Board, EnglishBoard, HexBoard, DiamondBoard


class Game(ABC): # absract base class
    def __init__(self, board):
        self.board = board

    def is_game_over(self):
        return not self.board.has_valid_moves()
    
    def display(self):
        self.board.display()

    @abstractmethod
    def play(self):
        pass

class ManualGame(Game):
    def make_move(self, start, end):
        if self.board.is_valid_move(start, end):
            self.board.apply_move(start, end)
        else:
            print("Invalid move. Try again.")
        
    def play(self):
        while not self.is_game_over():
            self.display()
            move = input("Enter over (r1 c1 r2 c2): ").split()
            r1, c1, r2, c2 = map(int, move)
            self.make_move((r1, c1), (r2, c2))

        print("Manual Game Over!")

class AutomatedGame(Game):
    def make_auto_move(self):
        moves = self.board.get_all_valid_moves()
        if moves:
            move = random.choice(moves)
            self.board.apply_move(*move)

    def play(self):
        while not self.is_game_over():
            self.display()
            self.make_auto_move()

        print("Automated Game Over!")
