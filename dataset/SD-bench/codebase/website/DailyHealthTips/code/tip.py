class Tip:
    def __init__(self, content: str, date: str):
        self.content = content
        self.date = date

    def save(self) -> None:
        with open('tips.txt', 'a') as file:
            file.write(f"{self.content}|{self.date}\n")

    @staticmethod
    def load_all() -> list:
        tips = []
        try:
            with open('tips.txt', 'r') as file:
                for line in file:
                    content, date = line.strip().split('|')
                    tips.append(Tip(content, date))
        except FileNotFoundError:
            return tips
        return tips