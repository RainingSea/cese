import json

class AdviceManager:
    def __init__(self):
        self.advice = self.load_advice()

    def load_advice(self):
        try:
            with open('advice.txt', 'r') as file:
                return [json.loads(line) for line in file.readlines()]
        except FileNotFoundError:
            return []

    def post_advice(self, title: str, content: str) -> bool:
        advice_data = {'title': title, 'content': content}
        self.advice.append(advice_data)
        self.save_advice()
        return True

    def get_advice(self) -> list:
        return self.advice

    def save_advice(self):
        with open('advice.txt', 'w') as file:
            for advice in self.advice:
                file.write(json.dumps(advice) + '\n')