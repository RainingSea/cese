from user import User
from blog_post import BlogPost

class BlogManager:
    def register_user(self, username: str, password: str, email: str) -> bool:
        user = User(username, password, email)
        user.save()
        return True

    def login(self, username: str, password: str) -> bool:
        with open('users.txt', 'r') as file:
            for line in file:
                u, p, _ = line.strip().split('|')
                if u == username and p == password:
                    return True
        return False

    def create_post(self, title: str, content: str, username: str) -> None:
        post_id = self.get_next_post_id()
        post = BlogPost(post_id, title, content, username)
        post.save()

    def view_posts(self, username: str) -> list:
        posts = []
        with open('posts.txt', 'r') as file:
            for line in file:
                post_id, title, content, user = line.strip().split('|')
                if user == username:
                    posts.append(BlogPost(int(post_id), title, content, user))
        return posts

    def get_post(self, post_id: int) -> BlogPost:
        with open('posts.txt', 'r') as file:
            for line in file:
                id_, title, content, username = line.strip().split('|')
                if int(id_) == post_id:
                    return BlogPost(int(id_), title, content, username)
        return None

    def edit_post(self, post_id: int, title: str, content: str) -> None:
        post = self.get_post(post_id)
        if post:
            post.edit(title, content)

    def delete_post(self, post_id: int) -> None:
        post = self.get_post(post_id)
        if post:
            post.delete(post_id)

    def get_next_post_id(self) -> int:
        try:
            with open('posts.txt', 'r') as file:
                lines = file.readlines()
                if lines:
                    last_line = lines[-1]
                    last_id = int(last_line.split('|')[0])
                    return last_id + 1
        except FileNotFoundError:
            return 1
        return 1