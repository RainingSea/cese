class Post:
    def __init__(self, username: str, title: str, content: str):
        self.username = username
        self.title = title
        self.content = content

    def save(self) -> None:
        with open('posts.txt', 'a') as file:
            file.write(f"{self.username},{self.title},{self.content}\n")

    def edit(self, title: str, content: str) -> None:
        self.title = title
        self.content = content
        self.save()

class PostManager:
    def __init__(self, posts_file: str):
        self.posts_file = posts_file
        self.posts = self.load_posts()

    def load_posts(self):
        posts = []
        try:
            with open(self.posts_file, 'r') as file:
                for line in file:
                    username, title, content = line.strip().split(',')
                    posts.append(Post(username, title, content))
        except FileNotFoundError:
            pass
        return posts

    def create_post(self, username: str, title: str, content: str) -> None:
        post = Post(username, title, content)
        post.save()
        self.posts.append(post)  # Update in-memory list

    def get_post(self, title: str) -> Post:
        for post in self.posts:
            if post.title == title:
                return post
        return None

    def edit_post(self, title: str, new_title: str, new_content: str) -> None:
        for post in self.posts:
            if post.title == title:
                post.edit(new_title, new_content)
                break

    def delete_post(self, title: str) -> None:
        self.posts = [post for post in self.posts if post.title != title]
        with open(self.posts_file, 'w') as file:
            for post in self.posts:
                file.write(f"{post.username},{post.title},{post.content}\n")