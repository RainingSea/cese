class TipManager:
    def __init__(self):
        self.tips = []
        self.current_index = 0

    def load_tips(self):
        try:
            with open('tips.txt', 'r') as file:
                self.tips = [line.strip() for line in file]
        except FileNotFoundError:
            print("Tips data file not found. Starting with an empty tips list.")

    def get_current_tip(self) -> str:
        if self.tips:
            return self.tips[self.current_index]
        return "No tips available."

    def previous_tip(self) -> None:
        if self.current_index > 0:
            self.current_index -= 1

    def next_tip(self) -> None:
        if self.current_index < len(self.tips) - 1:
            self.current_index += 1

    def search_tips(self, query: str) -> list:
        return [tip for tip in self.tips if query.lower() in tip.lower()]