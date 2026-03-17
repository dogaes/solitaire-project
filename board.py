class Board:
    def __init__(self, size=7, board_type="Engloish"):
        self.size = size
        self.board_type = board_type
        self.board = self.create_board()

    def create_board(self):
        board = [[1 for _ in range(self.size)] for _ in range(self.size)]

        # center empty like solitaire
        center = self.size // 2
        board[center][center] = 0

        return board
    
    def display_board(self):
        self.board = self.create_board()
        