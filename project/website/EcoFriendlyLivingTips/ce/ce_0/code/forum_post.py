class ForumPost:
    def __init__(self, username: str, content: str):
        self.username = username
        self.content = content

    def save(self):
        with open('forum_posts.txt', 'a') as f:
            f.write(f"{self.username}|{self.content}\n")

    @staticmethod
    def load_posts() -> list:
        posts = []
        try:
            with open('forum_posts.txt', 'r') as f:
                for line in f:
                    username, content = line.strip().split('|')
                    posts.append(ForumPost(username, content))
        except FileNotFoundError:
            pass
        return posts