class Post:
    def __init__(self, post_id: int, username: str, title: str, content: str):
        self.post_id = post_id
        self.username = username
        self.title = title
        self.content = content

    def save(self):
        with open('posts.txt', 'a') as f:
            f.write(f"{self.post_id}|{self.username}|{self.title}|{self.content}\n")

    @staticmethod
    def load_posts() -> list:
        posts = []
        try:
            with open('posts.txt', 'r') as f:
                for line in f:
                    post_id, username, title, content = line.strip().split('|')
                    posts.append(Post(int(post_id), username, title, content))
        except FileNotFoundError:
            pass
        return posts