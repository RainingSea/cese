class Tip:
    def __init__(self, content: str, date: str):
        self.content = content
        self.date = date

    @staticmethod
    def load_all() -> list:
        tips = []
        try:
            with open('tips.txt', 'r') as file:
                for line in file:
                    content, date = line.strip().split('|')
                    tips.append(Tip(content, date))
        except FileNotFoundError:
            pass
        return tips

    def search(self, query: str) -> list:
        return [tip for tip in self.load_all() if query.lower() in tip.content.lower()]