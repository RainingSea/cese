class PostManager:
    def __init__(self, posts_file: str):
        self.posts_file = posts_file
        self.load_posts()

    def load_posts(self):
        self.posts = []
        try:
            with open(self.posts_file, 'r') as file:
                for line in file:
                    title, content, username = line.strip().split('|')
                    self.posts.append({'title': title, 'content': content, 'username': username})
        except FileNotFoundError:
            open(self.posts_file, 'w').close()  # Create file if it does not exist

    def create_post(self, title: str, content: str, username: str) -> bool:
        with open(self.posts_file, 'a') as file:
            file.write(f"{title}|{content}|{username}\n")
        self.posts.append({'title': title, 'content': content, 'username': username})
        return True

    def get_posts(self) -> list:
        return self.posts

    def get_post(self, post_id: int) -> dict:
        if 0 <= post_id < len(self.posts):
            return self.posts[post_id]
        return None

    def edit_post(self, post_id: int, title: str, content: str) -> bool:
        if 0 <= post_id < len(self.posts):
            self.posts[post_id]['title'] = title
            self.posts[post_id]['content'] = content
            self.save_posts()
            return True
        return False

    def delete_post(self, post_id: int) -> bool:
        if 0 <= post_id < len(self.posts):
            del self.posts[post_id]
            self.save_posts()
            return True
        return False

    def save_posts(self):
        with open(self.posts_file, 'w') as file:
            for post in self.posts:
                file.write(f"{post['title']}|{post['content']}|{post['username']}\n")