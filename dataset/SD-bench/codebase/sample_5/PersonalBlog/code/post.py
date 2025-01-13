class Post:
    def __init__(self, title: str, content: str, username: str):
        self.title = title
        self.content = content
        self.username = username

    def save(self) -> None:
        with open('posts.txt', 'a') as f:
            f.write(f"{self.title}|{self.content}|{self.username}\n")

    @staticmethod
    def load_posts() -> list:
        posts = []
        try:
            with open('posts.txt', 'r') as f:
                for line in f:
                    title, content, username = line.strip().split('|')
                    posts.append(Post(title, content, username))
        except FileNotFoundError:
            pass
        return posts

    def edit(self, new_title: str, new_content: str) -> None:
        self.title = new_title
        self.content = new_content