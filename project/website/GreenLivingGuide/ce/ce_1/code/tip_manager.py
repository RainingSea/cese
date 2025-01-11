class TipManager:
    def __init__(self):
        self.tips = self.load_tips()

    def load_tips(self) -> list:
        tips = []
        try:
            with open('tips.txt', 'r') as file:
                tips = [line.strip() for line in file]
        except FileNotFoundError:
            pass
        return tips

    def save_tips(self) -> bool:
        try:
            with open('tips.txt', 'w') as file:
                for tip in self.tips:
                    file.write(f"{tip}\n")
            return True
        except Exception as e:
            print(f"Error saving tips: {e}")
            return False

    def add_tip(self, tip: str) -> bool:
        self.tips.append(tip)
        return self.save_tips()