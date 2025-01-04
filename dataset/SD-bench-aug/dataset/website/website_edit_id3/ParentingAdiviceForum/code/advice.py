class Advice:
    def __init__(self, title: str, content: str):
        self.title = title
        self.content = content

    def save(self):
        with open('advice.txt', 'a') as file:
            file.write(f"{self.title}|{self.content}\n")

    @staticmethod
    def load_all():
        advice_list = []
        with open('advice.txt', 'r') as file:
            for line in file:
                title, content = line.strip().split('|')
                advice_list.append(Advice(title, content))
        return advice_list