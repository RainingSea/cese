class BlogPost:
    def __init__(self, title: str, content: str, author: str):
        self.title = title
        self.content = content
        self.author = author

    def save(self):
        with open('posts.txt', 'a') as file:
            file.write(f"{self.title}|{self.content}|{self.author}\n")

    @staticmethod
    def load(post_id: int):
        # This method is not used in the current context but can be implemented if needed.
        pass

    @staticmethod
    def delete(post_id: int):
        # This method is not used in the current context but can be implemented if needed.
        pass