class TipManager:
    def __init__(self, tips_file: str):
        self.tips_file = tips_file
        self.load_tips()

    def load_tips(self):
        self.tips = []
        with open(self.tips_file, 'r') as file:
            for line in file:
                self.tips.append(line.strip())

    def get_current_tip(self) -> str:
        return self.tips[0] if self.tips else "No tips available."

    def get_previous_tip(self, current_index: int) -> str:
        if current_index > 0:
            return self.tips[current_index - 1]
        return "No previous tips."

    def get_next_tip(self, current_index: int) -> str:
        if current_index < len(self.tips) - 1:
            return self.tips[current_index + 1]
        return "No next tips."

    def get_all_tips(self) -> list:
        return self.tips

    def search_tips(self, query: str) -> list:
        return [tip for tip in self.tips if query.lower() in tip.lower()]