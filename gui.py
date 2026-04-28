import tkinter as tk
from tkinter import messagebox, filedialog
from board import EnglishBoard, HexBoard, DiamondBoard
from game import ManualGame, AutomatedGame
from recorder import GameRecorder, GameReplayer

class SolitaireGUI:
    def __init__(self, root, size=None, mode=None):
        self.root = root
        self.root.title("Solitaire")

        self.board = None
        self.game = None
        self.buttons = []
        self.selected = None
        self.mode = None
        self._game_over_timer = None
        self._autoplay_timer = None
        self.replayer = None
        self.replay_status = None

        self.recorder = GameRecorder()
        self.record_var = tk.BooleanVar(value=False)

        self.setup_menu(mode)

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def cancel_timers(self):
        if self._game_over_timer:
            self.root.after_cancel(self._game_over_timer)
            self._game_over_timer = None
        if self._autoplay_timer:
            self.root.after_cancel(self._autoplay_timer)
            self._autoplay_timer = None

    def setup_menu(self, mode=None):
        self.cancel_timers()
        self.game = None
        self.board = None
        self.selected = None
        self.mode = None
        self.replayer = None
        self.replay_status = None
        self.recorder.stop()
        self.clear_window()

        tk.Label(self.root, text="Solitaire", font=("Arial", 24)).pack(pady=20)

        # board size
        size_frame = tk.Frame(self.root)
        size_frame.pack(pady=10)
        tk.Label(size_frame, text="Board Size:").pack(side=tk.LEFT)
        self.size_var = tk.StringVar(value="7")
        tk.Radiobutton(size_frame, text="7", variable=self.size_var, value="7").pack(side=tk.LEFT)
        tk.Radiobutton(size_frame, text="9", variable=self.size_var, value="9").pack(side=tk.LEFT)

        # board type
        type_frame = tk.LabelFrame(self.root, text="Board Type")
        type_frame.pack(pady=10)
        self.type_var = tk.StringVar(value="English")
        for bt in ["English", "Hexagon", "Diamond"]:
            tk.Radiobutton(type_frame, text=bt, variable=self.type_var, value=bt).pack(anchor=tk.W)

        # game mode
        mode_frame = tk.LabelFrame(self.root, text="Game Mode")
        mode_frame.pack(pady=10)
        self.mode_var = tk.StringVar(value="Manual")
        tk.Radiobutton(mode_frame, text="Manual", variable=self.mode_var, value="Manual").pack(anchor=tk.W)
        tk.Radiobutton(mode_frame, text="Automated", variable=self.mode_var, value="Automated").pack(anchor=tk.W)

        # record option
        tk.Checkbutton(self.root, text="Record Game", variable=self.record_var).pack(pady=10)

        # buttons
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=20)
        tk.Button(btn_frame, text="New Game", width=12, command=self.new_game_from_menu).pack(side=tk.LEFT, padx=10)
        tk.Button(btn_frame, text="Replay", width=12, command=self.load_replay).pack(side=tk.LEFT, padx=10)

    def new_game_from_menu(self):
        board_type = self.type_var.get()
        size = int(self.size_var.get())
        mode = self.mode_var.get()
        self.start_game(board_type, size, mode)

    # game setup

    def start_game(self, board_type, size, mode, replay=False):
        self.mode = mode

        BOARD_CLASSES = {
            "English": EnglishBoard,
            "Hexagon": HexBoard,
            "Diamond": DiamondBoard
        }
        self.board = BOARD_CLASSES[board_type](size)
        
        # start recording if enabled and not replaying
        if self.record_var.get() and not replay:
            self.recorder.start(board_type, size, self.board.grid)
            recorder_arg = self.recorder
        else:
            self.recorder.stop()
            recorder_arg = None

        if mode == "Manual":
            self.game = ManualGame(self.board, recorder=recorder_arg)
        elif mode == "Automated":
            self.game = AutomatedGame(self.board, recorder=recorder_arg)

        self.create_board_ui()
        self.update_display()
        self.add_controls()

        if mode == "Automated" and not replay:
            self._autoplay_timer = self.root.after(1000, self.autoplay)  # start autoplay after 1 second

    # board gui

    def create_board_ui(self):
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
        frame.grid(row=self.board.size + 1, column=0, columnspan=self.board.size, pady=10)

        tk.Button(frame, text="New Game", command=self.setup_menu).pack(side=tk.LEFT, padx=10)
        tk.Button(frame, text="Randomize", command=self.randomize_board).pack(side=tk.LEFT, padx=10)
        tk.Button(frame, text="Autoplay", command=self.autoplay).pack(side=tk.LEFT, padx=10)

        # only show save button if recording
        if self.recorder.recording:
            tk.Button(frame, text="Save Recording", command=self.save_recording).pack(side=tk.LEFT, padx=10)

    # display

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

    # game actions

    def on_click(self, r, c):
        if self.game is None or self.board is None:
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
                self.game.make_move(start, end)     # recorder logs inside make_move

            self.selected = None
            self.update_display()

            if self.game.is_game_over():
                self.show_game_over()

    def randomize_board(self):
        if self.game is None or self.board is None:
            return
        self.board.randomize()
        if self.recorder.recording:
            self.recorder.log_randomize(self.board.grid)
        self.update_display()
        if self.game.is_game_over():
            self.show_game_over()

    def autoplay(self):
        if self.game is None or self.board is None:
            return
        if self.mode != "Automated":
            popup = tk.Toplevel(self.root)
            popup.title("Autoplay Not Available")
            popup.resizable(False, False)
            tk.Label(popup, text="Autoplay is only available in Automated mode.", padx=20, pady=20).pack()
            tk.Button(popup, text="OK", command=popup.destroy).pack(pady=(0, 10))
            popup.grab_set()
            return
        if not self.game.is_game_over():
            self.game.make_auto_move()   # recorder logs inside make_auto_move
            self.update_display()
            self._autoplay_timer = self.root.after(1000, self.autoplay)  # continue autoplay after 1 second
        else:
            self.show_game_over()

    def show_game_over(self):

        # auto save if recording
        if self.recorder.recording:
            filepath = self.recorder.save()
            messagebox.showinfo("Game Over", f"Game Over! Pegs remaining: {self.board.count_pegs()}\nRecording saved to: {filepath}")

        self.clear_window()
        pegs = self.board.count_pegs()
        tk.Label(self.root, text="Game Over!", font=("Arial", 24)).pack(pady=20)
        tk.Label(self.root, text=f"Pegs remaining: {pegs}", font=("Arial", 18)).pack(pady=10)
        tk.Label(self.root, text="No more valid moves", font=("Arial", 14)).pack(pady=10)
        tk.Button(self.root, text="Back to Menu", command=self.setup_menu).pack(pady=10)
        self._game_over_timer = self.root.after(5000, self.setup_menu)  # auto-return to menu after 5 seconds

    # recording

    def save_recording(self):
        if not self.recorder.events:
            messagebox.showwarning("Nothing to Save", "No moves have been recorded yet")
            return
        filepath = filedialog.asksaveasfilename(
            defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            title="Save Recording"
        )
        if filepath:
            saved = self.recorder.save(filepath)
            messagebox.showinfo("Saved", f"Recording saved to:\n{saved}")

            # refresh controls so save button disappears after saving
            self.add_controls()

    # replay

    def load_replay(self):
        filepath = filedialog.askopenfilename(
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            title="Open recording"
        )
        if not filepath:
            return
        try:
            self.replayer = GameReplayer(filepath)
        except Exception as e:
            messagebox.showerror("Error", f"Could not load recording:\n{e}")
            return

        init = self.replayer.get_init()
        if not init:
            messagebox.showerror("Error", "Recording file has no init event")
            return

        self.start_game(init["board_type"], init["board_size"], "Manual", replay=True)
        for r in range(self.board.size):
            for c in range(self.board.size):
                self.board.grid[r][c] = init["grid"][r][c]
        self.update_display()
        self.replay_controller = ReplayController(
            self.board, self.replayer, self.update_display, self.replay_status
        )
        self.add_replay_controls()

    def add_replay_controls(self):
        # remove existing control row and add replay specific controls
        for widget in self.root.grid_slaves(row=self.board.size + 1):
            widget.destroy()

        frame = tk.Frame(self.root)
        frame.grid(row=self.board.size + 1, column=0, columnspan=self.board.size, pady=6)
        self.replay_status = tk.Label(frame, text="Replay mode - press Next to step")
        self.replay_status.pack(side=tk.LEFT, padx=8)

        tk.Button(frame, text="Next", command=self.replay_controller.step).pack(side=tk.LEFT, padx=4)
        tk.Button(frame, text="Auto Replay", command=self.replay_auto).pack(side=tk.LEFT, padx=4)
        tk.Button(frame, text="Menu", command=self.replay_menu).pack(side=tk.LEFT, padx=4)

class ReplayController:
    def __init__(self, board, replayer, update_display, replay_status):
        self.board = board
        self.replayer = replayer
        self.update_display = update_display
        self.replay_status = replay_status

    def step(self):
        if not self.replayer.has_next():
            self.replay_status.config(text="Replay complete")
            return
        event = self.replayer.next_event()
        if event["type"] == "move":
            start = tuple(event["data"]["start"])
            end = tuple(event["data"]["end"])
            self.board.apply_move(start, end)
            self.update_display()
        elif event["type"] == "randomize":
            grid = event["data"]["grid"]
            for r in range(self.board.size):
                for c in range(self.board.size):
                    self.board.grid[r][c] = grid[r][c]
            self.update_display()
            self.replay_status.config(text="Randomize applied")

def run_gui():
    root = tk.Tk()
    app = SolitaireGUI(root)
    root.mainloop()
