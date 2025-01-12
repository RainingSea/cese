class TipManager:
    def __init__(self, tips_file):
        self.tips_file = tips_file
        self.tips = self.load_tips()

    def get_tip(self, index: int) -> str:
        if 0 <= index < len(self.tips):
            return self.tips[index]
        return "No tip available."

    def get_all_tips(self) -> list:
        return self.tips

    def search_tips(self, query: str) -> list:
        return [tip for tip in self.tips if query.lower() in tip.lower()]

    def load_tips(self) -> list:
        tips = []
        try:
            with open(self.tips_file, 'r') as file:
                for line in file:
                    tips.append(line.strip())
        except FileNotFoundError:
            pass
        return tips