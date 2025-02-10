class Post:
    def __init__(self, username: str, title: str, content: str):
        self.username = username
        self.title = title
        self.content = content

    def save(self) -> None:
        with open('posts.txt', 'a') as file:
            file.write(f"{self.username},{self.title},{self.content}\n")


class PostManager:
    def create_post(self, username: str, title: str, content: str) -> None:
        new_post = Post(username, title, content)
        new_post.save()

    def load_posts(self, username: str) -> list:
        posts = []
        try:
            with open('posts.txt', 'r') as file:
                for line in file:
                    user, title, content = line.strip().split(',')
                    if user == username:
                        posts.append(Post(user, title, content))
        except FileNotFoundError:
            pass
        return posts

    def edit_post(self, title: str, content: str) -> None:
        posts = self.load_all_posts()
        with open('posts.txt', 'w') as file:
            for post in posts:
                if post.title == title:
                    post.content = content
                file.write(f"{post.username},{post.title},{post.content}\n")

    def delete_post(self, title: str) -> None:
        posts = self.load_all_posts()
        with open('posts.txt', 'w') as file:
            for post in posts:
                if post.title != title:
                    file.write(f"{post.username},{post.title},{post.content}\n")

    def load_all_posts(self) -> list:
        posts = []
        try:
            with open('posts.txt', 'r') as file:
                for line in file:
                    username, title, content = line.strip().split(',')
                    posts.append(Post(username, title, content))
        except FileNotFoundError:
            pass
        return posts