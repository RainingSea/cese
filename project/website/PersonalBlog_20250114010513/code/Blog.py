from Post import Post

class Blog:
    def create_post(self, title: str, content: str) -> None:
        new_post = Post(title, content)
        new_post.save()

    def edit_post(self, old_title: str, new_title: str, new_content: str) -> None:
        posts = Post.load_posts()
        with open('posts.txt', 'w') as file:
            for post in posts:
                if post.title == old_title:
                    post.title = new_title
                    post.content = new_content
                file.write(f"{post.title}|{post.content}\n")

    def delete_post(self, title: str) -> None:
        posts = Post.load_posts()
        with open('posts.txt', 'w') as file:
            for post in posts:
                if post.title != title:
                    file.write(f"{post.title}|{post.content}\n")

    def get_posts(self) -> list:
        return Post.load_posts()