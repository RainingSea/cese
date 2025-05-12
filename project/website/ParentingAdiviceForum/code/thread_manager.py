class ThreadManager:
    def __init__(self):
        self.threads = self.load_threads()

    def load_threads(self):
        threads = []
        try:
            with open('threads.txt', 'r') as file:
                for line in file:
                    title, content, username = line.strip().split('|')
                    threads.append({'title': title, 'content': content, 'username': username})
        except FileNotFoundError:
            pass  # Handle the case where the file does not exist
        return threads

    def create_thread(self, title: str, content: str, username: str) -> bool:
        self.threads.append({'title': title, 'content': content, 'username': username})
        self.save_threads()
        return True

    def save_threads(self):
        with open('threads.txt', 'w') as file:
            for thread in self.threads:
                file.write(f"{thread['title']}|{thread['content']}|{thread['username']}\n")

    def get_threads(self) -> list:
        return self.threads

    def get_thread_details(self, thread_id: int) -> dict:
        return self.threads[thread_id] if 0 <= thread_id < len(self.threads) else {}