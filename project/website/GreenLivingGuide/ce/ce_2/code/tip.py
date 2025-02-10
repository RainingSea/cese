class Tip:
    def __init__(self, content: str):
        self.content = content

    def save(self):
        with open('tips.txt', 'a') as file:
            file.write(f"{self.content}\n")

    @staticmethod
    def load_all() -> list:
        tips = []
        try:
            with open('tips.txt', 'r') as file:
                for line in file:
                    tips.append(Tip(line.strip()))
        except FileNotFoundError:
            pass
        return tips