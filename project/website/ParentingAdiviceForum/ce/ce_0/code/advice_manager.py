class AdviceManager:
    def __init__(self):
        self.advice = self.load_advice()

    def load_advice(self):
        advice = []
        with open('advice.txt', 'r') as file:
            for line in file:
                title, content = line.strip().split('|')
                advice.append((title, content))
        return advice

    def post_advice(self, title: str, content: str) -> bool:
        self.advice.append((title, content))
        with open('advice.txt', 'a') as file:
            file.write(f"{title}|{content}\n")
        return True