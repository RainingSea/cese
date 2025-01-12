class ForumPost:
    def __init__(self, username: str, content: str):
        self.username = username
        self.content = content

    def save(self):
        with open('forum.txt', 'a') as f:
            f.write(f"{self.username}|{self.content}\n")

    @staticmethod
    def load_forum_posts():
        posts = []
        try:
            with open('forum.txt', 'r') as f:
                for line in f:
                    username, content = line.strip().split('|')
                    posts.append({'username': username, 'content': content})
        except FileNotFoundError:
            pass
        return posts