import os

class AdviceManager:
    def __init__(self):
        self.advices = self.load_advices()

    def load_advices(self):
        if not os.path.exists('advice.txt'):
            return []
        with open('advice.txt', 'r') as file:
            return [line.strip().split('|') for line in file.readlines()]

    def post_advice(self, title: str, content: str) -> bool:
        self.advices.append([title, content])
        self.save_advices()
        return True

    def save_advices(self):
        with open('advice.txt', 'w') as file:
            for advice in self.advices:
                file.write('|'.join(advice) + '\n')

    def get_advices(self) -> list:
        return self.advices