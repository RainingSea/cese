import os

class HistoryManager:
    def __init__(self, history_file: str):
        self.history_file = history_file

    def save_history(self, conversion: str):
        with open(self.history_file, "a") as file:
            file.write(conversion + "\n")

    def load_history(self) -> list:
        if not os.path.exists(self.history_file):
            return []
        with open(self.history_file, "r") as file:
            return file.read().strip().split("\n")

    def clear_history(self):
        open(self.history_file, "w").close()