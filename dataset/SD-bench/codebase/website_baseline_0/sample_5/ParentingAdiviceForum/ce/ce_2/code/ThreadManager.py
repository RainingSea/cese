import json
import os

class ThreadManager:
    def __init__(self, data_file='threads.txt'):
        self.data_file = data_file
        self.load_threads()

    def load_threads(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as file:
                self.threads = [json.loads(line.strip()) for line in file.readlines()]
        else:
            self.threads = []

    def create_thread(self, title: str, content: str) -> bool:
        thread_id = len(self.threads) + 1
        thread = {'id': thread_id, 'title': title, 'content': content}
        self.threads.append(thread)
        self.save_threads()
        return True

    def get_threads(self) -> list:
        return self.threads

    def get_thread_details(self, thread_id: int) -> dict:
        for thread in self.threads:
            if thread['id'] == thread_id:
                return thread
        return {}

    def save_threads(self):
        with open(self.data_file, 'w') as file:
            for thread in self.threads:
                file.write(json.dumps(thread) + '\n')