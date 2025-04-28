class TipManager:
    def __init__(self, filename: str):
        self.filename = filename
        self.tips = self.load_tips()
        self.current_index = 0

    def load_tips(self):
        with open(self.filename, 'r') as file:
            return [line.strip() for line in file]

    def get_current_tip(self) -> str:
        if self.tips:
            return self.tips[self.current_index]
        return "No tips available."

    def get_previous_tip(self, current_index: int) -> str:
        if current_index > 0:
            self.current_index -= 1
            return self.tips[self.current_index]
        return "No previous tips."

    def get_next_tip(self, current_index: int) -> str:
        if current_index < len(self.tips) - 1:
            self.current_index += 1
            return self.tips[self.current_index]
        return "No more tips."

    def search_tips(self, query: str) -> list:
        return [tip for tip in self.tips if query.lower() in tip.lower()]