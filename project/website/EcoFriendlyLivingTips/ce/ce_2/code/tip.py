class Tip:
    def __init__(self, title: str, content: str):
        self.title = title
        self.content = content

    def save(self):
        with open('tips.txt', 'a') as file:
            file.write(f"{self.title}|{self.content}\n")

    @staticmethod
    def load_all():
        tips = []
        with open('tips.txt', 'r') as file:
            for line in file:
                title, content = line.strip().split('|')
                tips.append(Tip(title, content))
        return tips