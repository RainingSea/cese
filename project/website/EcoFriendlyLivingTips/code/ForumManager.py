class ForumManager:
    def __init__(self):
        self.posts = self.load_posts()

    def load_posts(self):
        posts = []
        try:
            with open('forum.txt', 'r') as file:
                for line in file:
                    posts.append(line.strip())
        except FileNotFoundError:
            pass  # Handle the case where the file does not exist
        return posts

    def add_post(self, post: str) -> bool:
        self.posts.append(post)
        self.save_posts()
        return True

    def get_posts(self) -> list:
        return self.posts

    def save_posts(self):
        with open('forum.txt', 'w') as file:
            for post in self.posts:
                file.write(f"{post}\n")