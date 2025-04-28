import json

class ThreadManager:
    def __init__(self):
        self.threads = self.load_threads()

    def load_threads(self):
        try:
            with open('threads.txt', 'r') as file:
                return [json.loads(line) for line in file.readlines()]
        except FileNotFoundError:
            return []

    def create_thread(self, title: str, content: str) -> bool:
        thread_id = len(self.threads) + 1
        thread = {'id': thread_id, 'title': title, 'content': content}
        self.threads.append(thread)
        self.save_threads()
        return True

    def get_threads(self) -> list:
        return self.threads

    def get_thread(self, thread_id: int) -> dict:
        for thread in self.threads:
            if thread['id'] == thread_id:
                return thread
        return {}

    def save_threads(self):
        with open('threads.txt', 'w') as file:
            for thread in self.threads:
                file.write(json.dumps(thread) + '\n')