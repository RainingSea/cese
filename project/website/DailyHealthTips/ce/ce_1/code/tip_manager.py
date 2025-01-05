class TipManager:
    def __init__(self, filename: str):
        self.filename = filename
        self.tips = self.load_tips()

    def get_daily_tip(self) -> str:
        return self.tips[0] if self.tips else "No tips available today."

    def get_previous_tip(self, current_index: int) -> str:
        if current_index > 0:
            return self.tips[current_index - 1]
        return None

    def get_next_tip(self, current_index: int) -> str:
        if current_index < len(self.tips) - 1:
            return self.tips[current_index + 1]
        return None

    def load_tips(self) -> list:
        tips = []
        with open(self.filename, 'r') as file:
            for line in file:
                if line.strip():
                    tips.append(line.strip())
        return tips