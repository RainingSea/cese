class ForumManager:
    def __init__(self):
        self.posts = self.load_posts()

    def load_posts(self) -> list:
        posts = []
        try:
            with open('forum.txt', 'r') as file:
                posts = [line.strip() for line in file]
        except FileNotFoundError:
            pass
        return posts

    def save_posts(self) -> bool:
        try:
            with open('forum.txt', 'w') as file:
                for post in self.posts:
                    file.write(f"{post}\n")
            return True
        except Exception as e:
            print(f"Error saving posts: {e}")
            return False

    def add_post(self, post: str) -> bool:
        self.posts.append(post)
        return self.save_posts()