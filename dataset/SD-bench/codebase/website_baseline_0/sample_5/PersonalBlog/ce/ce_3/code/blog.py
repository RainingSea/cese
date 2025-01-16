from post import Post

class Blog:
    def create_post(self, title: str, content: str, author: str) -> None:
        new_post = Post(title, content, author)
        new_post.save()

    def edit_post(self, title: str, content: str, post_id: int) -> None:
        posts = Post.load_posts()
        if 0 <= post_id < len(posts):
            posts[post_id].title = title
            posts[post_id].content = content
            with open('posts.txt', 'w') as file:
                for post in posts:
                    file.write(f'{post.title}|{post.content}|{post.author}\n')

    def delete_post(self, post_id: int) -> None:
        posts = Post.load_posts()
        if 0 <= post_id < len(posts):
            del posts[post_id]
            with open('posts.txt', 'w') as file:
                for post in posts:
                    file.write(f'{post.title}|{post.content}|{post.author}\n')

    def get_posts_by_user(self, username: str) -> list:
        posts = Post.load_posts()
        return [post for post in posts if post.author == username]