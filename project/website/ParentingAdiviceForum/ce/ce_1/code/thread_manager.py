class ThreadManager:
    def __init__(self, filename):
        self.filename = filename
        self.load_threads()

    def load_threads(self):
        self.threads = []
        with open(self.filename, 'r') as file:
            for line in file:
                title, content, comments = line.strip().split('|')
                self.threads.append({'title': title, 'content': content, 'comments': comments.split(',')})

    def create_thread(self, title, content):
        self.threads.append({'title': title, 'content': content, 'comments': []})
        with open(self.filename, 'a') as file:
            file.write(f"{title}|{content}|\n")
        return True

    def get_threads(self):
        return self.threads

    def get_thread(self, thread_id):
        return self.threads[thread_id] if 0 <= thread_id < len(self.threads) else None

    def add_comment(self, thread_id, comment):
        if 0 <= thread_id < len(self.threads):
            self.threads[thread_id]['comments'].append(comment)
            self.save_threads()
            return True
        return False

    def save_threads(self):
        with open(self.filename, 'w') as file:
            for thread in self.threads:
                comments = ','.join(thread['comments'])
                file.write(f"{thread['title']}|{thread['content']}|{comments}\n")