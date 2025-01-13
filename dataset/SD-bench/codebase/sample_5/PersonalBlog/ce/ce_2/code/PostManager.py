class Post:
    def __init__(self, username: str, title: str, content: str):
        self.username = username
        self.title = title
        self.content = content

    def save(self) -> None:
        with open('posts.txt', 'a') as file:
            file.write(f"{self.username},{self.title},{self.content}\n")

    def edit(self, new_title: str, new_content: str) -> None:
        self.title = new_title
        self.content = new_content
        self.save()

    def delete(self) -> None:
        pass  # Deletion is handled in PostManager


class PostManager:
    def create_post(self, username: str, title: str, content: str) -> None:
        post = Post(username, title, content)
        post.save()

    def load_posts(self) -> list:
        posts = []
        try:
            with open('posts.txt', 'r') as file:
                for line in file:
                    username, title, content = line.strip().split(',')
                    posts.append(Post(username, title, content))
        except FileNotFoundError:
            pass
        return posts

    def get_post(self, title: str) -> Post:
        posts = self.load_posts()
        for post in posts:
            if post.title == title:
                return post
        return None

    def delete_post(self, title: str) -> None:
        posts = self.load_posts()
        with open('posts.txt', 'w') as file:
            for post in posts:
                if post.title != title:
                    file.write(f"{post.username},{post.title},{post.content}\n")