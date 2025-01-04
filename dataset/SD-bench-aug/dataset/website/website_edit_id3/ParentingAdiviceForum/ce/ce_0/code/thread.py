class Thread:
    def __init__(self, title: str, content: str):
        self.title = title
        self.content = content

    def save(self):
        with open('threads.txt', 'a') as f:
            f.write(f"{self.title}|{self.content}\n")

    @classmethod
    def load_all(cls):
        threads = []
        try:
            with open('threads.txt', 'r') as f:
                for line in f:
                    title, content = line.strip().split('|')
                    threads.append(cls(title, content))
        except FileNotFoundError:
            pass
        return threads

    @classmethod
    def load(cls, thread_id: int):
        threads = cls.load_all()
        if 0 <= thread_id < len(threads):
            return threads[thread_id]
        return None