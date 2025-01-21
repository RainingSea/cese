from post import Post

class Blog:
    def create_post(self, title: str, content: str, author: str):
        new_post = Post(title, content, author)
        new_post.save()

    def edit_post(self, title: str, content: str):
        posts = Post.load_posts()
        for post in posts:
            if post.title == title:
                post.content = content
                self.save_all(posts)
                break

    def delete_post(self, title: str):
        posts = Post.load_posts()
        posts = [post for post in posts if post.title != title]
        self.save_all(posts)

    def view_post(self, title: str) -> str:
        posts = Post.load_posts()
        for post in posts:
            if post.title == title:
                return post.content
        return "Post not found."

    def save_all(self, posts):
        with open('posts.txt', 'w') as file:
            for post in posts:
                file.write(f"{post.title}|{post.content}|{post.author}\n")