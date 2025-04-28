class TipManager:
    def __init__(self):
        self.tips = self.load_tips()

    def load_tips(self):
        tips = []
        with open('tips.txt', 'r') as file:
            for line in file:
                tips.append(line.strip())
        return tips

    def submit_tip(self, tip: str) -> bool:
        self.tips.append(tip)
        with open('tips.txt', 'a') as file:
            file.write(f"{tip}\n")
        return True

    def get_tips(self):
        return self.tips