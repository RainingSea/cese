import os

class ForumManager:
    def __init__(self):
        self.posts = self.load_posts()

    def load_posts(self):
        if not os.path.exists('forum.txt'):
            return []
        with open('forum.txt', 'r') as file:
            return [line.strip() for line in file.readlines()]

    def view_posts(self) -> list:
        return self.posts

    def submit_post(self, post: str) -> bool:
        self.posts.append(post)
        with open('forum.txt', 'a') as file:
            file.write(f"{post}\n")
        return True