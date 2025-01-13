class BlogPost:
    def __init__(self, title: str, content: str, author: str):
        self.title = title
        self.content = content
        self.author = author

    def create_post(self, title: str, content: str, author: str) -> None:
        with open('posts.txt', 'a') as file:
            file.write(f"{title}|{content}|{author}\n")

    def edit_post(self, title: str, content: str) -> None:
        posts = self.load_posts()
        with open('posts.txt', 'w') as file:
            for post in posts:
                if post[0] == title:
                    file.write(f"{title}|{content}|{self.author}\n")
                else:
                    file.write('|'.join(post) + '\n')

    def delete_post(self) -> None:
        posts = self.load_posts()
        with open('posts.txt', 'w') as file:
            for post in posts:
                if post[0] != self.title:
                    file.write('|'.join(post) + '\n')

    def view_post(self) -> str:
        return f"{self.title}\n{self.content}\nBy: {self.author}"

    @staticmethod
    def load_posts() -> list:
        posts = []
        try:
            with open('posts.txt', 'r') as file:
                for line in file:
                    posts.append(line.strip().split('|'))
        except FileNotFoundError:
            return posts
        return posts