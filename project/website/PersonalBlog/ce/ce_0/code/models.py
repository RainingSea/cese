from utils import load_data, save_data

class User:
    """Represents a user in the system."""
    def __init__(self, username: str, password: str, email: str):
        self.username = username
        self.password = password
        self.email = email

    def save(self):
        """Save user data to users.txt."""
        users = self.load_users()
        users.append({'username': self.username, 'password': self.password, 'email': self.email})
        save_data('users.txt', users)

    @staticmethod
    def load_users():
        """Load users from users.txt."""
        return load_data('users.txt')


class BlogPost:
    """Represents a blog post."""
    def __init__(self, title: str, content: str, author: str):
        self.title = title
        self.content = content
        self.author = author

    def save(self):
        """Save blog post data to posts.txt."""
        posts = self.load_posts()
        posts.append({'title': self.title, 'content': self.content, 'author': self.author})
        save_data('posts.txt', posts)

    @staticmethod
    def load_posts():
        """Load posts from posts.txt."""
        return load_data('posts.txt')

    def delete(self):
        """Delete a blog post."""
        posts = self.load_posts()
        posts = [post for post in posts if post['title'] != self.title]
        save_data('posts.txt', posts)

    def update(self, title: str, content: str):
        """Update a blog post."""
        posts = self.load_posts()
        for post in posts:
            if post['title'] == self.title:
                post['title'] = title
                post['content'] = content
        save_data('posts.txt', posts)