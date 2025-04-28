class BlogManager:
    def __init__(self, posts_file: str):
        self.posts_file = posts_file
        self.load_posts()

    def load_posts(self):
        self.posts = {}
        try:
            with open(self.posts_file, 'r') as file:
                for line in file:
                    username, title, content = line.strip().split('|')
                    if username not in self.posts:
                        self.posts[username] = []
                    self.posts[username].append((title, content))
        except FileNotFoundError:
            pass

    def create_post(self, username: str, title: str, content: str) -> bool:
        if username not in self.posts:
            self.posts[username] = []
        self.posts[username].append((title, content))
        with open(self.posts_file, 'a') as file:
            file.write(f"{username}|{title}|{content}\n")
        return True

    def get_posts(self, username: str) -> list:
        return self.posts.get(username, [])

    def edit_post(self, post_id: int, title: str, content: str) -> bool:
        # This method assumes the post_id is the index in the user's posts list
        username = list(self.posts.keys())[0]  # Simplified for this example
        if username in self.posts and 0 <= post_id < len(self.posts[username]):
            self.posts[username][post_id] = (title, content)
            self.save_posts()
            return True
        return False

    def delete_post(self, post_id: int) -> bool:
        username = list(self.posts.keys())[0]  # Simplified for this example
        if username in self.posts and 0 <= post_id < len(self.posts[username]):
            del self.posts[username][post_id]
            self.save_posts()
            return True
        return False

    def save_posts(self):
        with open(self.posts_file, 'w') as file:
            for username, posts in self.posts.items():
                for title, content in posts:
                    file.write(f"{username}|{title}|{content}\n")