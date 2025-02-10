class BlogPost:
    def __init__(self, post_id: int, title: str, content: str, username: str):
        self.post_id = post_id
        self.title = title
        self.content = content
        self.username = username

    def save(self):
        with open('posts.txt', 'a') as file:
            file.write(f"{self.post_id}|{self.title}|{self.content}|{self.username}\n")

    def delete(self, post_id: int):
        posts = []
        with open('posts.txt', 'r') as file:
            posts = file.readlines()
        with open('posts.txt', 'w') as file:
            for post in posts:
                if not post.startswith(f"{post_id}|"):
                    file.write(post)

    def edit(self, title: str, content: str):
        self.title = title
        self.content = content
        self.delete(self.post_id)
        self.save()