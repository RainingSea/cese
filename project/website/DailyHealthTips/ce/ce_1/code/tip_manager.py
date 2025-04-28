class TipManager:
    def __init__(self):
        self.tips = self.load_tips()

    def load_tips(self):
        tips = []
        with open('tips.txt', 'r') as file:
            for line in file:
                tips.append(line.strip())
        return tips

    def get_current_tip(self) -> str:
        return self.tips[0] if self.tips else "No tips available."

    def get_previous_tip(self) -> str:
        return self.tips[-1] if len(self.tips) > 1 else "No previous tips."

    def get_next_tip(self) -> str:
        return "No next tip available."

    def search_tips(self, query: str) -> list:
        return [tip for tip in self.tips if query.lower() in tip.lower()]