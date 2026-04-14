import json
import os
from datetime import datetime

class GameRecorder:
    # records moves and board events to a text file for later replay
    def __init__(self):
        self.events = []
        self.recording = False
    
    def start(self, board_type, board_size, initial_grid):
        # begin a new recording session
        self.events = []
        self.recording = True
        self.log_event("init", {
            "board_type": board_type,
            "board_size": board_size,
            "grid": [row[:] for row in initial_grid]  # deep copy of the grid
        })
    
    def log_move(self, start, end):
        if self.recording:
            self.log_event("move", {"start": list(start), "end": list(end)})

    def log_randomize(self, grid):
        if self.recording:
            self.log_event("randomize", {"grid": [row[:] for row in grid]})
        
    def log_event(self, event_type, data):
        self.events.append({"type": event_type, "data": data})
    
    def save(self, filepath=None):
        # save the recorded events to a JSON text file
        # returns the filepath of the saved recording
        if filepath is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filepath = f"game_{timestamp}.txt"
        with open(filepath, "w") as f:
            json.dump(self.events, f, indent=2)
        self.recording = False
        return filepath
    
    def stop(self):
        self.recording = False

class GameReplayer:
    # replays recorded game events from a text file
    def __init__(self, filepath):
        with open(filepath, "r") as f:
            self.events = json.load(f)
        self.index = 0      # points to the next event to replay
    
    def get_init(self):
        # returns the initial board setup from the recording
        for event in self.events:
            if event["type"] == "init":
                return event["data"]
        return None
    
    def has_next(self):
        # find next non-init event from current index
        for i in range(self.index, len(self.events)):
            if self.events[i]["type"] != "init":
                return True
        return False
        
    def next_event(self):
        # return the next non-init event dict, advancing the index
        while self.index < len(self.events):
            event = self.events[self.index]
            self.index += 1
            if event["type"] != "init":
                return event
        return None
    
    def reset(self):
        # reset the replay to the beginning (after init)
        self.index = 0