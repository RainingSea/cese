class ForumPost:
    def __init__(self, username: str, content: str):
        self.username = username
        self.content = content

    def save(self):
        with open('forum.txt', 'a') as file:
            file.write(f"{self.username}|{self.content}\n")