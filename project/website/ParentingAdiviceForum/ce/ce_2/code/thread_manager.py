class ThreadManager:
    def __init__(self):
        self.threads = self.load_threads()

    def load_threads(self):
        threads = {}
        try:
            with open('threads.txt', 'r') as file:
                for line in file:
                    thread_id, title, content = line.strip().split('|')
                    threads[thread_id] = {'title': title, 'content': content, 'comments': []}
        except FileNotFoundError:
            pass
        return threads

    def create_thread(self, title: str, content: str) -> bool:
        thread_id = str(len(self.threads) + 1)
        self.threads[thread_id] = {'title': title, 'content': content, 'comments': []}
        self.save_threads()
        return True

    def get_threads(self) -> list:
        return [{'id': thread_id, 'title': thread['title']} for thread_id, thread in self.threads.items()]

    def get_thread_details(self, thread_id: str) -> dict:
        return self.threads.get(thread_id)

    def add_comment(self, thread_id: str, comment: str) -> bool:
        if thread_id not in self.threads:
            return False
        self.threads[thread_id]['comments'].append(comment)
        self.save_threads()
        return True

    def save_threads(self):
        with open('threads.txt', 'w') as file:
            for thread_id, thread in self.threads.items():
                file.write(f"{thread_id}|{thread['title']}|{thread['content']}\n")