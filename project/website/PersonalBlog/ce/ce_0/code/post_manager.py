class Post:
    def __init__(self, post_id: int, title: str, content: str, author: str):
        self.post_id = post_id
        self.title = title
        self.content = content
        self.author = author

    def save(self):
        with open('posts.txt', 'a') as f:
            f.write(f"{self.post_id}|{self.title}|{self.content}|{self.author}\n")


class PostManager:
    def create_post(self, title: str, content: str, author: str) -> None:
        post_id = len(self.load_posts())
        post = Post(post_id, title, content, author)
        post.save()

    def load_posts(self) -> list:
        posts = []
        try:
            with open('posts.txt', 'r') as f:
                for line in f:
                    post_id, title, content, author = line.strip().split('|')
                    posts.append(Post(int(post_id), title, content, author))
        except FileNotFoundError:
            pass
        return posts

    def edit_post(self, post_id: int, title: str, content: str) -> None:
        posts = self.load_posts()
        if 0 <= post_id < len(posts):
            posts[post_id].title = title
            posts[post_id].content = content
            self.save_all(posts)

    def save_all(self, posts: list) -> None:
        with open('posts.txt', 'w') as f:
            for post in posts:
                f.write(f"{post.post_id}|{post.title}|{post.content}|{post.author}\n")

    def delete_post(self, post_id: int) -> None:
        posts = self.load_posts()
        if 0 <= post_id < len(posts):
            del posts[post_id]
            self.save_all(posts)