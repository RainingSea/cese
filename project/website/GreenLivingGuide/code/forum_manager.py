import os

class ForumManager:
    def __init__(self):
        self.posts = self.load_posts()

    def load_posts(self) -> list:
        """Load forum posts from the forum_posts.txt file."""
        posts = []
        try:
            with open('forum_posts.txt', 'r') as file:
                posts = [line.strip() for line in file]
        except FileNotFoundError:
            pass
        return posts

    def save_posts(self) -> None:
        """Save forum posts to the forum_posts.txt file."""
        with open('forum_posts.txt', 'w') as file:
            for post in self.posts:
                file.write(f"{post}\n")

    def add_post(self, post: str) -> None:
        """Add a new post and save to the file."""
        self.posts.append(post)
        self.save_posts()

    def get_posts(self) -> list:
        """Retrieve all forum posts."""
        return self.posts

    def verify_post_data(self) -> bool:
        """Verify if post data is correctly saved."""
        current_posts = self.load_posts()
        return current_posts == self.posts