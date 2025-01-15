from models import Post

class Blog:
    def create_post(self, username: str, title: str, content: str) -> None:
        new_post = Post(username, title, content)
        new_post.save()

    def edit_post(self, post_id: int, title: str, content: str) -> None:
        posts = Post.load_posts()
        if 0 <= post_id < len(posts):
            posts[post_id].title = title
            posts[post_id].content = content
            self.save_all(posts)

    def delete_post(self, post_id: int) -> None:
        posts = Post.load_posts()
        if 0 <= post_id < len(posts):
            del posts[post_id]
            self.save_all(posts)

    def get_posts(self, username: str) -> list:
        return [post for post in Post.load_posts() if post.username == username]

    def get_post(self, post_id: int) -> Post:
        posts = Post.load_posts()
        if 0 <= post_id < len(posts):
            return posts[post_id]
        return None

    @staticmethod
    def save_all(posts: list) -> None:
        with open('posts.txt', 'w') as file:
            for post in posts:
                file.write(f"{post.username},{post.title},{post.content}\n")