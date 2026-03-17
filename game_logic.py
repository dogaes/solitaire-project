from board import Board

class GameLogic:
    def __init__(self):
        self.board = None

    def start_game(self, size=7, board_type="English"):
        self.board = Board(size, board_type)

    def make_move(self, start, end):

        r1, c1 = start
        r2, c2 = end

        if self.validate_move(start, end):

            mid_r = (r1 + r2) // 2
            mid_c = (c1 + c2) // 2

            self.board.board[r1][c1] = 0
            self.board.board[mid_r][mid_c] = 0
            self.board.board[r2][c2] = 1

            return True
        return False
    
    def validate_move(self, start, end):
        r1, c1 = start
        r2, c2 = end

        if self.board.board[r1][c1] != 1:
            return False
        if self.board.board[r2][c2] != 0:
            return False
        if abs(r1 - r2) == 2 and c1 == c2:
            return True
        if abs(c1 - c2) == 2 and r1 == r2:
            return True
        return False
    
    def check_game_over(self):

        board = self.board.board
        for r in range(self.board.size):
            for c in range(self.board.size):

                if board[r][c] == 1:
                    directions = [(0, 2), (0, -2), (2, 0), (-2, 0)]
                    for dr, dc in directions:
                        r2 = r + dr
                        c2 = c + dc
                        if 0 <= r2 < self.board.size and 0 <= c2 < self.board.size:
                            if board[r2][c2] == 0:
                                return False
        return True
    
    def check_win(self):
        count = 0

        for row in self.board.board:
            count += row.count(1)

        return count == 1

