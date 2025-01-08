class BlogPost:
    def __init__(self, post_id: int, title: str, content: str):
        self.post_id = post_id
        self.title = title
        self.content = content

    def save(self):
        with open('posts.txt', 'a') as file:
            file.write(f"{self.post_id}|{self.title}|{self.content}\n")

    @staticmethod
    def load_all() -> list:
        posts = []
        try:
            with open('posts.txt', 'r') as file:
                for line in file:
                    post_id, title, content = line.strip().split('|')
                    posts.append(BlogPost(int(post_id), title, content))
        except FileNotFoundError:
            pass
        return posts

    @staticmethod
    def delete(post_id: int):
        posts = BlogPost.load_all()
        with open('posts.txt', 'w') as file:
            for post in posts:
                if post.post_id != post_id:
                    file.write(f"{post.post_id}|{post.title}|{post.content}\n")


class Blog:
    def __init__(self):
        self.posts = BlogPost.load_all()
        self.next_post_id = len(self.posts) + 1

    def create_post(self, title: str, content: str):
        new_post = BlogPost(self.next_post_id, title, content)
        new_post.save()
        self.posts.append(new_post)
        self.next_post_id += 1

    def edit_post(self, post_id: int, title: str, content: str):
        for post in self.posts:
            if post.post_id == post_id:
                post.title = title
                post.content = content
                BlogPost.delete(post_id)
                post.save()
                break

    def view_post(self, post_id: int) -> BlogPost:
        for post in self.posts:
            if post.post_id == post_id:
                return post
        return None

    def list_posts(self) -> list:
        return self.posts