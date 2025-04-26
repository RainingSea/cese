class PostManager:
    def __init__(self, filename: str):
        self.filename = filename
        self.load_posts()

    def load_posts(self):
        self.posts = []
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                for line in f:
                    title, content, username = line.strip().split('|')
                    self.posts.append({'title': title, 'content': content, 'username': username})

    def create_post(self, username: str, title: str, content: str) -> bool:
        with open(self.filename, 'a') as f:
            f.write(f"{title}|{content}|{username}\n")
        self.posts.append({'title': title, 'content': content, 'username': username})
        return True

    def edit_post(self, post_id: int, title: str, content: str) -> bool:
        if post_id < 0 or post_id >= len(self.posts):
            return False
        self.posts[post_id]['title'] = title
        self.posts[post_id]['content'] = content
        self.save_posts()
        return True

    def delete_post(self, post_id: int) -> bool:
        if post_id < 0 or post_id >= len(self.posts):
            return False
        del self.posts[post_id]
        self.save_posts()
        return True

    def get_posts(self, username: str) -> list:
        return [post for post in self.posts if post['username'] == username]

    def get_post(self, post_id: int) -> str:
        if post_id < 0 or post_id >= len(self.posts):
            return ""
        post = self.posts[post_id]
        return f"Title: {post['title']}\nContent: {post['content']}"

    def save_posts(self):
        with open(self.filename, 'w') as f:
            for post in self.posts:
                f.write(f"{post['title']}|{post['content']}|{post['username']}\n")