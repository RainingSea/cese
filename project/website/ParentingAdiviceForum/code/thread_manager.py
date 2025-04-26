class ThreadManager:
    def __init__(self):
        self.threads = self.load_threads()

    def load_threads(self):
        threads = []
        try:
            with open('threads.txt', 'r') as file:
                for line in file:
                    thread_id, title, content = line.strip().split('|')
                    threads.append({'id': int(thread_id), 'title': title, 'content': content})
        except FileNotFoundError:
            pass  # Handle the case where the file does not exist
        return threads

    def create_thread(self, title: str, content: str) -> bool:
        thread_id = len(self.threads) + 1
        self.threads.append({'id': thread_id, 'title': title, 'content': content})
        self.save_threads()
        return True

    def get_threads(self) -> list:
        return self.threads

    def get_thread(self, thread_id: int) -> dict:
        for thread in self.threads:
            if thread['id'] == thread_id:
                return thread
        return None  # Return None if thread not found
    
    def save_threads(self):
        with open('threads.txt', 'w') as file:
            for thread in self.threads:
                file.write(f"{thread['id']}|{thread['title']}|{thread['content']}\n")