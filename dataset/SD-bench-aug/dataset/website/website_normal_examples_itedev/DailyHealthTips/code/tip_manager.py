class TipManager:
    def __init__(self, tips_file: str):
        self.tips_file = tips_file
        self.tips = self.load_tips()

    def load_tips(self) -> list:
        tips = []
        try:
            with open(self.tips_file, 'r') as file:
                for line in file:
                    if line.strip():  # Avoid empty lines
                        tips.append(line.strip())
        except FileNotFoundError:
            with open(self.tips_file, 'w'):  # Create file if not exists
                pass
        return tips

    def get_daily_tip(self) -> str:
        if self.tips:
            return self.tips[0]  # Return the first tip as the daily tip
        return "No tips available."

    def get_all_tips(self) -> list:
        return self.tips