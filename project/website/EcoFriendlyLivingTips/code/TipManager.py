class TipManager:
    def __init__(self):
        self.tips = self.load_tips()

    def load_tips(self):
        tips = []
        try:
            with open('tips.txt', 'r') as file:
                for line in file:
                    tips.append(line.strip())
        except FileNotFoundError:
            pass  # Handle the case where the file does not exist
        return tips

    def submit_tip(self, tip: str) -> bool:
        self.tips.append(tip)
        self.save_tips()
        return True

    def get_tips(self) -> list:
        return self.tips

    def save_tips(self):
        with open('tips.txt', 'w') as file:
            for tip in self.tips:
                file.write(f"{tip}\n")