class BlogPost:
    def __init__(self, post_id: int, title: str, content: str):
        self.post_id = post_id
        self.title = title
        self.content = content

    def save(self):
        with open('posts.txt', 'a') as f:
            f.write(f"{self.post_id}|{self.title}|{self.content}\n")

    @staticmethod
    def load_all() -> list:
        posts = []
        with open('posts.txt', 'r') as f:
            for line in f:
                post_id, title, content = line.strip().split('|')
                posts.append(BlogPost(int(post_id), title, content))
        return posts

    @staticmethod
    def delete(post_id: int):
        posts = BlogPost.load_all()
        with open('posts.txt', 'w') as f:
            for post in posts:
                if post.post_id != post_id:
                    f.write(f"{post.post_id}|{post.title}|{post.content}\n")


class Blog:
    def create_post(self, title: str, content: str):
        post_id = len(BlogPost.load_all()) + 1
        new_post = BlogPost(post_id, title, content)
        new_post.save()

    def edit_post(self, post_id: int, title: str, content: str):
        posts = BlogPost.load_all()
        with open('posts.txt', 'w') as f:
            for post in posts:
                if post.post_id == post_id:
                    post.title = title
                    post.content = content
                f.write(f"{post.post_id}|{post.title}|{post.content}\n")

    def view_post(self, post_id: int) -> BlogPost:
        posts = BlogPost.load_all()
        for post in posts:
            if post.post_id == post_id:
                return post
        return None

    def list_posts(self) -> list:
        return BlogPost.load_all()