class TipManager:
    def __init__(self):
        self.tips = []
        self.load_tips()

    def load_tips(self):
        try:
            with open('tips.txt', 'r') as file:
                self.tips = [line.strip() for line in file]
        except FileNotFoundError:
            pass

    def get_current_tip(self) -> str:
        return self.tips[0] if self.tips else "No tips available."

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