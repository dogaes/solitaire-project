from board import Board, EnglishBoard, HexBoard, DiamondBoard
from game import ManualGame, AutomatedGame
from gui import run_gui

def create_board(board_type, size, mode):
    if board_type == "English":
        return EnglishBoard(size)
    elif board_type == "Hexagon":
        return HexBoard(size)
    elif board_type == "Diamond":
        return DiamondBoard(size)
    else:
        raise ValueError("Invalid board type")
    
def main():
    while True:
        board_type = input("Select board type (English, Hexagon, Diamond): ")
        size = int(input("Select board size (7 or 9): "))
        mode = input("Select mode (Manual or Automated): ")

        board = create_board(board_type, size, mode)
        if board is None:
            continue
        if mode == "Manual":
            game = ManualGame(board)
        elif mode == "Automated":
            game = AutomatedGame(board)
        else:
            print("Invalid mode")
            continue
        game.play()
            
if __name__ == "__main__":
    run_gui()
