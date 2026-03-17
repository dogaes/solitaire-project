import tkinter as tk
from game_logic import GameLogic

class SolitaireGUI:

    def __init__(self):
        self.game = GameLogic()

        self.root = tk.Tk()
        self.root.title("Solitaire")

        self.size_var = tk.IntVar(value=7)
        self.board_type_var = tk.StringVar(value="English")

        self.create_controls()

        self.buttons = []

        self.root.mainloop()

    def create_controls(self):

        frame = tk.Frame(self.root)
        frame.pack()

        tk.Label(frame, text="Board Size:").pack()

        tk.Radiobutton(frame, text="7", variable=self.size_var, value=7).pack()
        tk.Radiobutton(frame, text="9", variable=self.size_var, value=9).pack()

        tk.Label(frame, text="Board Type:").pack()

        tk.Radiobutton(frame, text="English", variable=self.board_type_var, value="English").pack()
        tk.Radiobutton(frame, text="Diamond", variable=self.board_type_var, value="Diamond").pack()
        tk.Radiobutton(frame, text="Hexagon", variable=self.board_type_var, value="Hexagon").pack()

        tk.Button(frame, text="Start Game", command=self.start_game).pack()

        self.board_frame = tk.Frame(self.root)
        self.board_frame.pack()

    def start_game(self):
        size = self.size_var.get()
        board_type = self.board_type_var.get()

        self.game.start_game(size, board_type)

        self.draw_board()

    def draw_board(self):
        for widget in self.board_frame.winfo_children():
            widget.destroy()

        self.buttons = []

        for r in range(len(self.game.board.board)):
            row_buttons = []
            for c in range(self.game.board.size):
                text = "O" if self.game.board.board[r][c] == 1 else " "

                btn = tk.Button(self.board_frame, text=text, width=3, height=1, command=lambda r=r, c=c: self.select(r, c))
                btn.grid(row=r, column=c)
                row_buttons.append(btn)
            self.buttons.append(row_buttons)
            self.selected = None

        def select(self, r, c):
            if self.selected is None:
                self.selected = (r, c)
            else:
                success = self.game.make_move(self.selected, (r, c))

                self.selected = None

                self.draw_board()

                if self.game.check_game_over():
                    if self.game.check_win():
                        tk.messagebox.showinfo("You win!")
                    else:
                        tk.messagebox.showinfo("Game Over")
if __name__ == "__main__":
    SolitaireGUI()
    