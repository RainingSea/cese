class Post:
    def __init__(self, title: str, content: str, author: str) -> None:
        self.title = title
        self.content = content
        self.author = author

    def save(self) -> None:
        with open('posts.txt', 'a') as file:
            file.write(f'{self.title}|{self.content}|{self.author}\n')

    @staticmethod
    def load_posts() -> list:
        posts = []
        with open('posts.txt', 'r') as file:
            for line in file:
                title, content, author = line.strip().split('|')
                posts.append(Post(title, content, author))
        return posts