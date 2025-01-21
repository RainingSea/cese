class Post:
    def __init__(self, title: str, content: str, author: str, post_id: int):
        self.title = title
        self.content = content
        self.author = author
        self.post_id = post_id

    def save(self):
        with open('posts.txt', 'a') as f:
            f.write(f"{self.post_id}|{self.title}|{self.content}|{self.author}\n")

    @staticmethod
    def load(post_id: int):
        with open('posts.txt', 'r') as f:
            for line in f:
                post_data = line.strip().split('|')
                if int(post_data[0]) == post_id:
                    return Post(post_data[1], post_data[2], post_data[3], post_id)
        return None