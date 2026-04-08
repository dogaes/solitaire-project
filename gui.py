import tkinter as tk
from board import EnglishBoard, HexBoard, DiamondBoard
from game import ManualGame, AutomatedGame

class SolitaireGUI:
    def __init__(self, root, size, mode):
        self.root = root
        self.root.title("Solitaire")

        self.board = None
        self.game = None
        self.buttons = []
        self.selected = None
        self.setup_menu(mode)
    
    def setup_menu(self, mode = None):
        self.game = None
        self.board = None
        self.selected = None
        if hasattr(self, '_game_over_timer') and self.game_over_timer:
            self.root.after_cancel(self.game_over_timer)
            self.game_over_timer = None
        self.clear_window()

        tk.Label(self.root, text="Choose Board Size:").pack()
        tk.Button(self.root, text="7x7", command=lambda: self.choose_board_type(7)).pack()
        tk.Button(self.root, text="9x9", command=lambda: self.choose_board_type(9)).pack()

    def start_game(self, board_type, size, mode):
        size = int(size)
        self.mode = mode

        if board_type == "English":
            self.board = EnglishBoard(size)
        elif board_type == "Hexagon":
            self.board = HexBoard(size)
        elif board_type == "Diamond":
            self.board = DiamondBoard(size)

        if mode == "Manual":
            self.game = ManualGame(self.board)
        elif mode == "Automated":
            self.game = AutomatedGame(self.board)

        self.create_board()
        self.update_display()
        self.add_controls()

    def choose_board_type(self, size):
        self.clear_window()

        tk.Label(self.root, text="Choose Board Type:").pack()
        tk.Button(self.root, text="English", command=lambda: self.choose_mode("English", size)).pack()
        tk.Button(self.root, text="Hexagon", command=lambda: self.choose_mode("Hexagon", size)).pack()
        tk.Button(self.root, text="Diamond", command=lambda: self.choose_mode("Diamond", size)).pack()

    def choose_mode(self, board_type, size):
        self.clear_window()

        tk.Label(self.root, text="Choose Game Mode:").pack()
        tk.Button(self.root, text="Manual", command=lambda: self.start_game(board_type, size, "Manual")).pack()
        tk.Button(self.root, text="Automated", command=lambda: self.start_game(board_type, size, "Automated")).pack()

    def create_board(self):
        self.clear_window()
        self.buttons = []
        self.status_label = tk.Label(self.root, text="")
        self.status_label.grid(row=self.board.size, column=0, columnspan=self.board.size)

        for r in range(self.board.size):
            row = []
            for c in range(self.board.size):
                if self.board.grid[r][c] == -1:
                    btn = tk.Label(self.root, text="", width=4, height=2, bg="grey85", relief="flat")
                else:
                    btn = tk.Button(self.root, width=4, height=2, command=lambda r=r, c=c: self.on_click(r, c))    
                btn.grid(row=r, column=c)
                row.append(btn)
            self.buttons.append(row)

    def add_controls(self):
        frame = tk.Frame(self.root)
        frame.grid(row=self.board.size + 1, column=0, columnspan=self.board.size)

        tk.Button(frame, text="Randomize", command=self.randomize_board).pack(side=tk.LEFT)
        tk.Button(frame, text="Autoplay", command=self.autoplay).pack(side=tk.LEFT)
        tk.Button(frame, text="Menu", command=self.setup_menu).pack(side=tk.LEFT)
    
    def randomize_board(self):
        self.board.randomize()
        self.update_display()
        if self.game.is_game_over():
            self.show_game_over()
    
    def autoplay(self):
        if self.game is None or self.board is None:
            return
        if self.mode != "Automated":
            popup = tk.Toplevel(self.root)
            popup.title("Not available")
            popup.resizable(False, False)
            tk.Label(popup, text="Autoplay is only available in Automated mode.").pack(padx=20, pady=20)
            tk.Button(popup, text="OK", command=popup.destroy).pack(pady=10)
            popup.grab_set() # make it modal
            return

    def on_click(self, r, c):
        if self.game is None or self.mode is None:
            return
        if self.selected is None:
            if self.board.grid[r][c] == 1:
                self.selected = (r, c)
                self.buttons[r][c].config(bg="yellow")
            if self.board.grid[r][c] == -1:
                return
        else:
            start = self.selected
            end = (r, c)

            if self.board.is_valid_move(start, end):
                self.board.apply_move(start, end)
            
            self.selected = None
            self.update_display()


            if self.game.is_game_over():
                self.show_game_over()

    def update_display(self):
        for r in range(self.board.size):
            for c in range(self.board.size):
                val = self.board.grid[r][c]
                if val == -1:
                    continue
                if val == 1:
                    self.buttons[r][c].config(text="●", bg="SystemButtonFace")
                else:
                    self.buttons[r][c].config(text="◯", bg="SystemButtonFace")
        pegs = self.board.count_pegs()
        self.status_label.config(text=f"Pegs remaining: {pegs}")

    def show_game_over(self):
        self.clear_window()
        pegs = self.board.count_pegs()
        tk.Label(self.root, text="Game Over!", font=("Arial", 24)).pack(pady=20)
        tk.Label(self.root, text=f"Pegs remaining: {pegs}", font=("Arial", 18)).pack(pady=10)
        tk.Label(self.root, text="No more valid moves", font=("Arial", 14)).pack(pady=10)
        tk.Button(self.root, text="Back to Menu", command=self.setup_menu).pack(pady=10)
        self._game_over_timer = self.root.efter(5000, self.setup_menu)  # auto-return to menu after 5 seconds
    
    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

def run_gui():
    root = tk.Tk()
    app = SolitaireGUI(root, size=7, mode="Manual")  # default values, will be overridden by menu
    root.mainloop()