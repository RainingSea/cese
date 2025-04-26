class ThreadManager:
    def __init__(self):
        self.threads = self.load_threads()

    def load_threads(self):
        threads = []
        try:
            with open('threads.txt', 'r') as file:
                for line in file:
                    title, content = line.strip().split('|')
                    threads.append({'title': title, 'content': content})
        except FileNotFoundError:
            pass
        return threads

    def create_thread(self, title: str, content: str) -> bool:
        self.threads.append({'title': title, 'content': content})
        with open('threads.txt', 'a') as file:
            file.write(f"{title}|{content}\n")
        return True

    def get_threads(self) -> list:
        return self.threads

    def get_thread_details(self, thread_id: int) -> dict:
        if 0 <= thread_id < len(self.threads):
            return self.threads[thread_id]
        return {}