class ForumPost:
    def __init__(self, content: str):
        self.content = content

    def save(self):
        with open('forum_posts.txt', 'a') as file:
            file.write(f"{self.content}\n")

    @staticmethod
    def load_all() -> list:
        posts = []
        with open('forum_posts.txt', 'r') as file:
            for line in file:
                posts.append(ForumPost(line.strip()))
        return posts