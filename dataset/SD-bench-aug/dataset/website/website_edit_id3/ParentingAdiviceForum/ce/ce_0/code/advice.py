class Advice:
    def __init__(self, title: str, content: str):
        self.title = title
        self.content = content

    def save(self):
        with open('advice.txt', 'a') as f:
            f.write(f"{self.title}|{self.content}\n")

    @classmethod
    def load_all(cls):
        advices = []
        try:
            with open('advice.txt', 'r') as f:
                for line in f:
                    title, content = line.strip().split('|')
                    advices.append(cls(title, content))
        except FileNotFoundError:
            pass
        return advices