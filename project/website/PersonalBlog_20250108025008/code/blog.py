class BlogPost:
    def __init__(self, post_id: int, title: str, content: str):
        self.post_id = post_id
        self.title = title
        self.content = content

    def save(self):
        with open('posts.txt', 'a') as f:
            f.write(f"{self.post_id}|{self.title}|{self.content}\n")

    @staticmethod
    def load_all():
        posts = []
        try:
            with open('posts.txt', 'r') as f:
                for line in f:
                    post_id, title, content = line.strip().split('|')
                    posts.append(BlogPost(int(post_id), title, content))
        except FileNotFoundError:
            pass
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
        posts = BlogPost.load_all()
        post_id = len(posts) + 1
        new_post = BlogPost(post_id, title, content)
        new_post.save()

    def edit_post(self, post_id: int, new_title: str, new_content: str):
        posts = BlogPost.load_all()
        for post in posts:
            if post.post_id == post_id:
                post.title = new_title
                post.content = new_content
        with open('posts.txt', 'w') as f:
            for post in posts:
                f.write(f"{post.post_id}|{post.title}|{post.content}\n")

    def view_post(self, post_id: int) -> BlogPost:
        posts = BlogPost.load_all()
        for post in posts:
            if post.post_id == post_id:
                return post
        return None

    def list_posts(self):
        return BlogPost.load_all()