from user import User
from blog_post import BlogPost

class FileManager:
    def save_user(self, user: User) -> None:
        user.register(user.username, user.password, user.email)

    def load_users(self) -> list:
        return User.load_users()

    def save_post(self, post: BlogPost) -> None:
        post.create_post(post.title, post.content, post.author)

    def load_posts(self) -> list:
        return BlogPost.load_posts()