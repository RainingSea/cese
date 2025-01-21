class Post:
    def __init__(self, title: str, content: str, author: str):
        self.title = title
        self.content = content
        self.author = author

    def save(self):
        with open('posts.txt', 'a') as file:
            file.write(f"{self.title}|{self.content}|{self.author}\n")

    @staticmethod
    def load_posts():
        posts = []
        try:
            with open('posts.txt', 'r') as file:
                for line in file:
                    title, content, author = line.strip().split('|')
                    posts.append(Post(title, content, author))
        except FileNotFoundError:
            pass
        return posts