class ThreadManager:
    def __init__(self):
        self.threads = self.load_threads()

    def load_threads(self):
        threads = []
        with open('threads.txt', 'r') as file:
            for line in file:
                title, content = line.strip().split('|')
                threads.append((title, content))
        return threads

    def create_thread(self, title: str, content: str) -> bool:
        self.threads.append((title, content))
        with open('threads.txt', 'a') as file:
            file.write(f"{title}|{content}\n")
        return True

    def get_threads(self):
        return self.threads

    def get_thread_details(self, thread_id: int) -> str:
        return self.threads[thread_id] if 0 <= thread_id < len(self.threads) else None