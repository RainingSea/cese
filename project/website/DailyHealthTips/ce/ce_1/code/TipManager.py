import random

class TipManager:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.tips = self.load_tips()

    def get_daily_tip(self) -> str:
        return random.choice(self.tips) if self.tips else "No tips available."

    def get_previous_tip(self, current_index: int) -> str:
        if current_index > 0:
            return self.tips[current_index - 1]
        return "No previous tip."

    def get_next_tip(self, current_index: int) -> str:
        if current_index < len(self.tips) - 1:
            return self.tips[current_index + 1]
        return "No next tip."

    def search_tips(self, query: str) -> list:
        return [tip for tip in self.tips if query.lower() in tip.lower()]

    def load_tips(self) -> list:
        tips = []
        try:
            with open(self.file_path, 'r') as file:
                tips = [line.strip() for line in file]
        except FileNotFoundError:
            pass
        return tips