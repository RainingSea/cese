class BlogPost:
    def __init__(self, title: str, content: str, author: str):
        self.title = title
        self.content = content
        self.author = author

    def save(self):
        with open('posts.txt', 'a') as f:
            f.write(f'{self.title}|{self.content}|{self.author}\n')

    @staticmethod
    def load(post_id: int):
        with open('posts.txt', 'r') as f:
            for idx, line in enumerate(f):
                if idx == post_id:
                    post_data = line.strip().split('|')
                    return BlogPost(post_data[0], post_data[1], post_data[2])
        return None

    @staticmethod
    def delete(post_id: int):
        with open('posts.txt', 'r') as f:
            lines = f.readlines()
        with open('posts.txt', 'w') as f:
            for idx, line in enumerate(lines):
                if idx != post_id:
                    f.write(line)