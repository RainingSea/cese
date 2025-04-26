class TipManager:
    def __init__(self):
        self.tips = self.load_tips()
        self.current_index = 0

    def load_tips(self):
        tips = []
        with open('tips.txt', 'r') as file:
            for line in file:
                date, tip = line.strip().split(':', 1)
                tips.append((date, tip))
        return tips

    def get_current_tip(self) -> str:
        if self.tips:
            return self.tips[self.current_index][1]
        return "No tips available."

    def get_previous_tip(self) -> str:
        if self.current_index > 0:
            self.current_index -= 1
        return self.get_current_tip()

    def get_next_tip(self) -> str:
        if self.current_index < len(self.tips) - 1:
            self.current_index += 1
        return self.get_current_tip()

    def search_tips(self, query: str) -> list:
        return [tip for tip in self.tips if query in tip[1]]