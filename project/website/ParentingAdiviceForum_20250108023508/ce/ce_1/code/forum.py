class Comment:
    def __init__(self, content: str):
        self.content = content

class Thread:
    def __init__(self, title: str, content: str):
        self.title = title
        self.content = content
        self.comments = []

class Forum:
    def __init__(self):
        self.threads = self.load_threads()

    def load_threads(self):
        threads = []
        with open('threads.txt', 'r') as file:
            for line in file:
                title, content = line.strip().split('|')
                threads.append(Thread(title, content))
        return threads

    def add_thread(self, thread: Thread):
        self.threads.append(thread)
        with open('threads.txt', 'a') as file:
            file.write(f"{thread.title}|{thread.content}\n")

    def get_threads(self) -> list:
        return self.threads

    def get_thread_by_title(self, title: str) -> Thread:
        for thread in self.threads:
            if thread.title == title:
                return thread
        return None