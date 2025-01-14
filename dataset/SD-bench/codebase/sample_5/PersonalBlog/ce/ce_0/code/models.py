class User:
    def __init__(self, username: str, password: str, email: str):
        self.username = username
        self.password = password
        self.email = email

    def save(self):
        with open('users.txt', 'a') as file:
            file.write(f"{self.username},{self.password},{self.email}\n")

    @staticmethod
    def load_users() -> list:
        users = []
        try:
            with open('users.txt', 'r') as file:
                for line in file:
                    username, password, email = line.strip().split(',')
                    users.append(User(username, password, email))
        except FileNotFoundError:
            pass
        return users


class Post:
    def __init__(self, username: str, title: str, content: str):
        self.username = username
        self.title = title
        self.content = content

    def save(self):
        with open('posts.txt', 'a') as file:
            file.write(f"{self.username},{self.title},{self.content}\n")

    @staticmethod
    def load_posts() -> list:
        posts = []
        try:
            with open('posts.txt', 'r') as file:
                for line in file:
                    username, title, content = line.strip().split(',')
                    posts.append(Post(username, title, content))
        except FileNotFoundError:
            pass
        return posts