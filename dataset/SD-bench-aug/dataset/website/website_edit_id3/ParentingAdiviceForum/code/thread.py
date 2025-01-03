class Thread:
    def __init__(self, title: str, content: str):
        self.title = title
        self.content = content

    def save(self):
        with open('threads.txt', 'a') as file:
            file.write(f"{self.title}|{self.content}\n")

    @staticmethod
    def load_all():
        threads = []
        with open('threads.txt', 'r') as file:
            for line in file:
                title, content = line.strip().split('|')
                threads.append(Thread(title, content))
        return threads