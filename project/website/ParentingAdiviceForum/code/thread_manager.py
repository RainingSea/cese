import os

class ThreadManager:
    def __init__(self):
        self.threads = self.load_threads()

    def load_threads(self):
        if not os.path.exists('threads.txt'):
            return []
        with open('threads.txt', 'r') as file:
            return [line.strip().split('|') for line in file.readlines()]

    def create_thread(self, title: str, content: str) -> bool:
        thread_id = len(self.threads) + 1
        self.threads.append([str(thread_id), title, content])
        self.save_threads()
        return True

    def save_threads(self):
        with open('threads.txt', 'w') as file:
            for thread in self.threads:
                file.write('|'.join(thread) + '\n')

    def get_threads(self) -> list:
        return self.threads

    def get_thread_details(self, thread_id: int) -> dict:
        for thread in self.threads:
            if int(thread[0]) == thread_id:
                return {'id': thread[0], 'title': thread[1], 'content': thread[2]}
        return {}