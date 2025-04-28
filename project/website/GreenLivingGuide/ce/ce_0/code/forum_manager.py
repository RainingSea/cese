class ForumManager:
    def __init__(self):
        self.posts = self.load_posts()

    def load_posts(self):
        posts = []
        with open('forum_posts.txt', 'r') as file:
            for line in file:
                posts.append(line.strip())
        return posts

    def submit_post(self, post: str) -> bool:
        self.posts.append(post)
        with open('forum_posts.txt', 'a') as file:
            file.write(f"{post}\n")
        return True

    def get_posts(self):
        return self.posts