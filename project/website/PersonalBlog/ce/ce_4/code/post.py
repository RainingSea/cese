class Post:
    def __init__(self, title: str, content: str, author: str):
        self.title = title
        self.content = content
        self.author = author

    def save(self):
        with open('posts.txt', 'a') as f:
            f.write(f"{self.title}|{self.content}|{self.author}\n")

    @staticmethod
    def load_posts() -> list:
        posts = []
        try:
            with open('posts.txt', 'r') as f:
                for line in f:
                    title, content, author = line.strip().split('|')
                    posts.append(Post(title, content, author))
        except FileNotFoundError:
            pass
        return posts

    def delete(self):
        # Placeholder for delete functionality
        pass

    def edit(self, new_title: str, new_content: str):
        self.title = new_title
        self.content = new_content
        # Save changes to file (not implemented)