class TipManager:
    def __init__(self, tips_file: str):
        self.tips_file = tips_file
        self.tips = self.load_tips()
        self.current_index = 0

    def load_tips(self) -> list:
        tips = []
        try:
            with open(self.tips_file, 'r') as file:
                for line in file:
                    tips.append(line.strip())
        except FileNotFoundError:
            open(self.tips_file, 'w').close()  # Create file if it doesn't exist
        return tips

    def get_current_tip(self) -> str:
        return self.tips[self.current_index] if self.tips else "No tips available."

    def get_previous_tip(self) -> str:
        if self.current_index > 0:
            self.current_index -= 1
        return self.get_current_tip()

    def get_next_tip(self) -> str:
        if self.current_index < len(self.tips) - 1:
            self.current_index += 1
        return self.get_current_tip()

    def get_all_tips(self) -> list:
        return self.tips

    def search_tips(self, query: str) -> list:
        return [tip for tip in self.tips if query.lower() in tip.lower()]