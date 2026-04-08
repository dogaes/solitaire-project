import random

class Board:
    def __init__(self, size):
        self.size = size
        self.grid = self.create_board()

    def create_board(self):
        board = [[1 for _ in range(self.size)] for _ in range(self.size)]
        mid = self.size // 2
        board[mid][mid] = 0
        return board
    
    def display(self):
        for row in self.grid:
            print(" ".join(map(str, row)))
        print()
    
    def is_valid_move(self, start, end):
        r1, c1 = start
        r2, c2 = end

        if self.grid[r1][c1] != 1 or self.grid[r2][c2] != 0:
            return False
        
        if abs(r1 - r2) == 2 and c1 == c2:  # vertical move
            mid_r = (r1 + r2) // 2
            return (
                self.grid[r1][c1] == 1 and      # start has a peg
                self.grid[mid_r][c1] == 1 and   # middle has a peg
                self.grid[r2][c2] == 0          # end is empty
            )
        
        if abs(c1 - c2) == 2 and r1 == r2:  # horizontal move
            mid_c = (c1 + c2) // 2
            return (
                self.grid[r1][c1] == 1 and       # start has a peg
                self.grid[r1][mid_c] == 1 and    # middle has a peg
                self.grid[r2][c2] == 0           # end is empty
            )
        return False
    
    def apply_move(self, start, end):
        r1, c1 = start
        r2, c2 = end

        mid_r = (r1 + r2) // 2
        mid_c = (c1 + c2) // 2

        self.grid[r1][c1] = 0    # remove peg from start
        self.grid[mid_r][mid_c] = 0  # remove the jumped peg
        self.grid[r2][c2] = 1   # place peg at end

    def get_all_valid_moves(self):
        moves = []
        for r in range(self.size):
            for c in range(self.size):
                if self.grid[r][c] == 1:  # only consider moves from pegs
                    
                    # check 4 directions
                    directions = [(-2, 0), (2, 0), (0, -2), (0, 2)]
                    for dr, dc in directions:
                        r2, c2 = r + dr, c + dc
                        if 0 <= r2 < self.size and 0 <= c2 < self.size:
                            if self.is_valid_move((r, c), (r2, c2)):
                                moves.append(((r, c), (r2, c2)))
        return moves
    
    def has_valid_moves(self):
        return len(self.get_all_valid_moves()) > 0
    
    def randomize(self):
        import random
        for r in range(self.size):
            for c in range(self.size):
                if self.grid[r][c] != -1:  # only randomize valid positions
                    self.grid[r][c] = random.choice([0, 1])

    def count_pegs(self):
        return sum(row.count(1) for row in self.grid)

class EnglishBoard(Board):
    def create_board(self):
        board = [[1 for _ in range(self.size)] for _ in range(self.size)]
        
        cut = self.size // 2 - 1

        for r in range(self.size):
            for c in range(self.size):
                if (r < cut or r > self.size - cut - 1) and (c < cut or c > self.size - cut - 1):
                    board[r][c] = -1
        
        # center empty
        mid = self.size // 2                
        board[mid][mid] = 0
        return board
    

class HexBoard(Board):
    def create_board(self):
        board = [[-1 for _ in range(self.size)] for _ in range(self.size)]
        cut = self.size // 2 - 1
        mid = self.size // 2

        for r in range(self.size):
            for c in range(self.size):
                t1 = r + c < cut
                t2 = r + (self.size - 1 - c) < cut
                t3 = (self.size - 1 - r) + c < cut
                t4 = (self.size - 1 - r) + (self.size - 1 - c) < cut
                if not (t1 or t2 or t3 or t4):
                    board[r][c] = 1

        board[mid][mid] = 0
        return board

class DiamondBoard(Board):
    def create_board(self):
        board = [[-1 for _ in range(self.size)] for _ in range(self.size)]
        mid = self.size // 2

        for r in range(self.size):
            for c in range(self.size):
                if abs(r - mid) + abs(c - mid) <= mid:
                    board[r][c] = 1
        
        # center empty
        board[mid][mid] = 0
        return board


        