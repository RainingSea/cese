class Post:
    def __init__(self, title: str, content: str):
        self.title = title
        self.content = content

    def save(self) -> None:
        with open('posts.txt', 'a') as file:
            file.write(f"{self.title}|{self.content}\n")

    @staticmethod
    def load_posts() -> list:
        posts = []
        try:
            with open('posts.txt', 'r') as file:
                for line in file:
                    title, content = line.strip().split('|')
                    posts.append(Post(title, content))
        except FileNotFoundError:
            pass
        return posts