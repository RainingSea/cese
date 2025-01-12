class Post:
    def __init__(self, username: str, title: str, content: str):
        self.username = username
        self.title = title
        self.content = content

    def save(self):
        with open('posts.txt', 'a') as file:
            file.write(f"{self.username}:{self.title}:{self.content}\n")

    @staticmethod
    def load_all():
        posts = []
        try:
            with open('posts.txt', 'r') as file:
                for line in file:
                    username, title, content = line.strip().split(':')
                    posts.append(Post(username, title, content))
        except FileNotFoundError:
            pass
        return posts

    def delete(self):
        posts = Post.load_all()
        posts = [post for post in posts if not (post.username == self.username and post.title == self.title)]
        with open('posts.txt', 'w') as file:
            for post in posts:
                file.write(f"{post.username}:{post.title}:{post.content}\n")