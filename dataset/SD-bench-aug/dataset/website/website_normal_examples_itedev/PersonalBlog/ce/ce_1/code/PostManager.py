class PostManager:
    def __init__(self, posts_file: str):
        self.posts_file = posts_file
        self.load_posts()

    def load_posts(self):
        """Load posts from the specified file into memory."""
        self.posts = {}
        try:
            with open(self.posts_file, 'r') as file:
                for line in file:
                    title, content, username = line.strip().split('|')
                    if username not in self.posts:
                        self.posts[username] = []
                    self.posts[username].append({'title': title, 'content': content})
        except FileNotFoundError:
            pass

    def create_post(self, title: str, content: str, username: str) -> None:
        """Create a new blog post."""
        if username not in self.posts:
            self.posts[username] = []
        self.posts[username].append({'title': title, 'content': content})
        with open(self.posts_file, 'a') as file:
            file.write(f"{title}|{content}|{username}\n")

    def get_posts(self, username: str) -> list:
        """Retrieve all posts for a given user."""
        return self.posts.get(username, [])

    def get_post(self, title: str) -> dict:
        """Retrieve a specific post by title."""
        for username, posts in self.posts.items():
            for post in posts:
                if post['title'] == title:
                    return post
        return {}

    def edit_post(self, title: str, new_title: str, new_content: str) -> bool:
        """Edit an existing post."""
        for username, posts in self.posts.items():
            for post in posts:
                if post['title'] == title:
                    post['title'] = new_title
                    post['content'] = new_content
                    self.save_posts()
                    return True
        return False

    def delete_post(self, title: str) -> bool:
        """Delete a post by title."""
        for username, posts in self.posts.items():
            for post in posts:
                if post['title'] == title:
                    posts.remove(post)
                    self.save_posts()
                    return True
        return False

    def save_posts(self):
        """Save all posts back to the file."""
        with open(self.posts_file, 'w') as file:
            for username, posts in self.posts.items():
                for post in posts:
                    file.write(f"{post['title']}|{post['content']}|{username}\n")