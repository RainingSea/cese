class Tip:
    def __init__(self, content: str, date: str):
        self.content = content
        self.date = date

    @staticmethod
    def load_all() -> list:
        """Load all tips from the tips.txt file."""
        tips = []
        with open('tips.txt', 'r') as file:
            for line in file:
                content, date = line.strip().split('|')
                tips.append(Tip(content, date))
        return tips