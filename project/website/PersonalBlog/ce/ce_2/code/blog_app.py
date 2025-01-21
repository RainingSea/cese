from user import User
from post import Post

class BlogApp:
    def __init__(self):
        self.users = []
        self.posts = []
        self.load_users()
        self.load_posts()

    def load_users(self):
        with open('users.txt', 'r') as f:
            for line in f:
                user_data = line.strip().split('|')
                self.users.append(User(user_data[0], user_data[1], user_data[2]))

    def load_posts(self):
        with open('posts.txt', 'r') as f:
            for line in f:
                post_data = line.strip().split('|')
                self.posts.append(Post(post_data[1], post_data[2], post_data[3], int(post_data[0])))

    def register(self, username: str, password: str, email: str) -> str:
        new_user = User(username, password, email)
        new_user.save()
        self.users.append(new_user)
        return "Registration successful"

    def login(self, username: str, password: str) -> str:
        user = User.load(username)
        if user and user.password == password:
            return "Login successful"
        return "Invalid credentials"

    def create_post(self, title: str, content: str, author: str) -> str:
        post_id = len(self.posts) + 1
        new_post = Post(title, content, author, post_id)
        new_post.save()
        self.posts.append(new_post)
        return "Post created"

    def edit_post(self, post_id: int, title: str, content: str) -> str:
        post = Post.load(post_id)
        if post:
            post.title = title
            post.content = content
            self.save_posts()
            return "Post updated"
        return "Post not found"

    def delete_post(self, post_id: int) -> str:
        post = Post.load(post_id)
        if post:
            self.posts.remove(post)
            self.save_posts()
            return "Post deleted"
        return "Post not found"

    def get_posts(self, author: str) -> list:
        return [post for post in self.posts if post.author == author]

    def save_posts(self):
        with open('posts.txt', 'w') as f:
            for post in self.posts:
                f.write(f"{post.post_id}|{post.title}|{post.content}|{post.author}\n")