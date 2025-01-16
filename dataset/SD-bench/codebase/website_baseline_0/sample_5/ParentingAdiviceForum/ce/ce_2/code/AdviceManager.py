import json
import os

class AdviceManager:
    def __init__(self, data_file='advice.txt'):
        self.data_file = data_file
        self.load_advice()

    def load_advice(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as file:
                self.advice_list = [json.loads(line.strip()) for line in file.readlines()]
        else:
            self.advice_list = []

    def post_advice(self, title: str, content: str) -> bool:
        advice = {'title': title, 'content': content}
        self.advice_list.append(advice)
        self.save_advice()
        return True

    def get_advice(self) -> list:
        return self.advice_list

    def save_advice(self):
        with open(self.data_file, 'w') as file:
            for advice in self.advice_list:
                file.write(json.dumps(advice) + '\n')