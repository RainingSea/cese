import os
import time

class ContentController:
    def __init__(self):
        self.content_file = "content.txt"
        if not os.path.exists(self.content_file):
            open(self.content_file, 'w').close()

    def create_content(self, username, title, content_text):
        content_id = f"{int(time.time())}_{hash(username)}"
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        with open(self.content_file, 'a') as f:
            f.write(f"{content_id}|{username}|{title}|{content_text}|{timestamp}\n")
        return True

    def get_feed(self):
        feed = []
        if os.path.exists(self.content_file):
            with open(self.content_file, 'r') as f:
                for line in reversed(f.readlines()):
                    content_id, username, title, content_text, timestamp = line.strip().split('|')
                    feed.append({
                        'content_id': content_id,
                        'username': username,
                        'title': title,
                        'content': content_text,
                        'timestamp': timestamp
                    })
        return feed

    def get_content(self, content_id):
        if os.path.exists(self.content_file):
            with open(self.content_file, 'r') as f:
                for line in f:
                    c_id, username, title, content_text, timestamp = line.strip().split('|')
                    if c_id == content_id:
                        return {
                            'content_id': content_id,
                            'username': username,
                            'title': title,
                            'content': content_text,
                            'timestamp': timestamp
                        }
        return None