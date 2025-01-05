class TipManager:
    def __init__(self):
        self.tips = []
        self.load_tips()

    def get_current_tip(self) -> str:
        return self.tips[0] if self.tips else "No tips available."

    def load_tips(self) -> None:
        try:
            with open('tips.txt', 'r') as file:
                self.tips = [line.strip() for line in file]
        except FileNotFoundError:
            pass

    def save_tips(self) -> None:
        with open('tips.txt', 'w') as file:
            for tip in self.tips:
                file.write(f"{tip}\n")