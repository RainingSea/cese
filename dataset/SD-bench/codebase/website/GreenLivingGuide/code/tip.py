class Tip:
    def __init__(self, content: str):
        self.content = content

    def save(self):
        with open('tips.txt', 'a') as f:
            f.write(f"{self.content}\n")

    @staticmethod
    def load_tips():
        tips = []
        try:
            with open('tips.txt', 'r') as f:
                for line in f:
                    tips.append(line.strip())
        except FileNotFoundError:
            pass
        return tips