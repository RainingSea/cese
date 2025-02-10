class ForumManager:
    def __init__(self, filename: str):
        self.filename = filename
        self.posts = self.load_posts()

    def load_posts(self) -> list:
        posts = []
        try:
            with open(self.filename, 'r') as file:
                posts = [line.strip() for line in file]
        except FileNotFoundError:
            pass
        return posts

    def submit_post(self, post: str) -> None:
        with open(self.filename, 'a') as file:
            file.write(f"{post}\n")
        self.posts.append(post)