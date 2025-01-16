from user import User
from blog_post import BlogPost

class BlogManager:
    def __init__(self, users_file: str, posts_file: str):
        self.users_file = users_file
        self.posts_file = posts_file
        self.users = self.load_users()
        self.posts = self.load_posts()

    def load_users(self):
        users = []
        try:
            with open(self.users_file, 'r') as file:
                for line in file:
                    username, password, email = line.strip().split('|')
                    users.append(User(username, password, email))
        except FileNotFoundError:
            pass  # Handle the case where the file does not exist
        return users

    def load_posts(self):
        posts = []
        try:
            with open(self.posts_file, 'r') as file:
                for line in file:
                    title, content, author = line.strip().split('|')
                    posts.append(BlogPost(title, content, author))
        except FileNotFoundError:
            pass  # Handle the case where the file does not exist
        return posts

    def register_user(self, username: str, password: str, email: str) -> bool:
        if any(user.username == username for user in self.users):
            return False
        new_user = User(username, password, email)
        self.users.append(new_user)
        with open(self.users_file, 'a') as file:
            file.write(new_user.to_string() + '\n')
        return True

    def login_user(self, username: str, password: str) -> bool:
        return any(user.username == username and user.password == password for user in self.users)

    def create_post(self, title: str, content: str, author: str) -> None:
        new_post = BlogPost(title, content, author)
        self.posts.append(new_post)
        with open(self.posts_file, 'a') as file:
            file.write(new_post.to_string() + '\n')

    def get_posts(self) -> list:
        return self.posts

    def get_post(self, title: str) -> BlogPost:
        for post in self.posts:
            if post.title == title:
                return post
        return None

    def edit_post(self, title: str, new_title: str, new_content: str) -> None:
        for post in self.posts:
            if post.title == title:
                post.title = new_title
                post.content = new_content
                self.save_posts()
                break

    def delete_post(self, title: str) -> None:
        self.posts = [post for post in self.posts if post.title != title]
        self.save_posts()

    def save_posts(self) -> None:
        with open(self.posts_file, 'w') as file:
            for post in self.posts:
                file.write(post.to_string() + '\n')