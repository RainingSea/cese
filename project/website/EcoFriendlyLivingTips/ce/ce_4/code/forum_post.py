class ForumPost:
    def __init__(self, content: str):
        self.content = content

    def save(self):
        with open('forum.txt', 'a') as file:
            file.write(f"{self.content}\n")

    @staticmethod
    def load_all():
        forum_posts = []
        with open('forum.txt', 'r') as file:
            for line in file:
                forum_posts.append(ForumPost(line.strip()))
        return forum_posts