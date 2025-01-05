class TipManager:
    def __init__(self):
        self.tips = []
        self.current_index = 0

    def get_current_tip(self) -> str:
        if self.tips:
            return self.tips[self.current_index]
        return "No tips available."

    def get_previous_tip(self, current_index: int) -> str:
        if current_index > 0:
            return self.tips[current_index - 1]
        return "No previous tip."

    def get_next_tip(self, current_index: int) -> str:
        if current_index < len(self.tips) - 1:
            return self.tips[current_index + 1]
        return "No next tip."

    def load_tips(self) -> None:
        try:
            with open('tips.txt', 'r') as f:
                self.tips = [line.strip() for line in f.readlines()]
        except FileNotFoundError:
            pass

    def save_tips(self) -> None:
        with open('tips.txt', 'w') as f:
            for tip in self.tips:
                f.write(f"{tip}\n")