class ForumPost:
    def __init__(self, username: str, content: str):
        self.username = username
        self.content = content

    def save(self):
        with open('forum.txt', 'a') as file:
            file.write(f"{self.username}|{self.content}\n")

    @staticmethod
    def load_all():
        posts = []
        with open('forum.txt', 'r') as file:
            for line in file:
                username, content = line.strip().split('|')
                posts.append(ForumPost(username, content))
        return posts