class TipManager:
    def __init__(self, filename: str):
        self.filename = filename
        self.tips = self.load_tips()

    def get_daily_tip(self) -> str:
        return self.tips[0] if self.tips else "No tips available."

    def load_tips(self) -> list:
        tips = []
        try:
            with open(self.filename, 'r') as file:
                for line in file:
                    tips.append(line.strip())
        except FileNotFoundError:
            pass
        return tips