from post import Post

class Blog:
    def create_post(self, username: str, title: str, content: str) -> None:
        post_id = len(Post.load_posts()) + 1
        new_post = Post(post_id, username, title, content)
        new_post.save()

    def edit_post(self, post_id: int, title: str, content: str) -> None:
        posts = Post.load_posts()
        for post in posts:
            if post.post_id == post_id:
                post.title = title
                post.content = content
                self.save_all(posts)
                break

    def delete_post(self, post_id: int) -> None:
        posts = Post.load_posts()
        posts = [post for post in posts if post.post_id != post_id]
        self.save_all(posts)

    def get_posts(self, username: str) -> list:
        return [post for post in Post.load_posts() if post.username == username]

    def get_post(self, post_id: int) -> Post:
        posts = Post.load_posts()
        for post in posts:
            if post.post_id == post_id:
                return post
        return None

    def save_all(self, posts: list) -> None:
        with open('posts.txt', 'w') as f:
            for post in posts:
                f.write(f"{post.post_id}|{post.username}|{post.title}|{post.content}\n")