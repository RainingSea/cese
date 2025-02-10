class Thread:
    def __init__(self, title: str, content: str):
        self.title = title
        self.content = content

    def save(self) -> None:
        with open('threads.txt', 'a') as f:
            f.write(f"{self.title}|{self.content}\n")

    @staticmethod
    def load_all() -> list:
        threads = []
        try:
            with open('threads.txt', 'r') as f:
                for line in f:
                    title, content = line.strip().split('|')
                    threads.append(Thread(title, content))
        except FileNotFoundError:
            pass
        return threads