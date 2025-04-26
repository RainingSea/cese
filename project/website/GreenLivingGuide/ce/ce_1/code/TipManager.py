import os

class TipManager:
    def __init__(self):
        self.tips = self.load_tips()

    def load_tips(self):
        if not os.path.exists('tips.txt'):
            return []
        with open('tips.txt', 'r') as file:
            return [line.strip() for line in file.readlines()]

    def view_tips(self) -> list:
        return self.tips

    def submit_tip(self, tip: str) -> bool:
        self.tips.append(tip)
        with open('tips.txt', 'a') as file:
            file.write(f"{tip}\n")
        return True