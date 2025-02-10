class TipManager:
    def __init__(self, filename: str):
        self.filename = filename
        self.tips = self.load_tips()

    def load_tips(self) -> list:
        tips = []
        try:
            with open(self.filename, 'r') as file:
                tips = [line.strip() for line in file]
        except FileNotFoundError:
            pass
        return tips

    def submit_tip(self, tip: str) -> None:
        with open(self.filename, 'a') as file:
            file.write(f"{tip}\n")
        self.tips.append(tip)