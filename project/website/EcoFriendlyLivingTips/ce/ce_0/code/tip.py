class Tip:
    def __init__(self, title: str, description: str):
        self.title = title
        self.description = description

    def save(self):
        with open('tips.txt', 'a') as f:
            f.write(f"{self.title}|{self.description}\n")

    @staticmethod
    def load_tips() -> list:
        tips = []
        try:
            with open('tips.txt', 'r') as f:
                for line in f:
                    title, description = line.strip().split('|')
                    tips.append(Tip(title, description))
        except FileNotFoundError:
            pass
        return tips