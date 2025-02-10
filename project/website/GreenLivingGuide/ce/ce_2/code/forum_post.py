class ForumPost:
    def __init__(self, username: str, message: str):
        self.username = username
        self.message = message

    def save(self):
        with open('forum.txt', 'a') as file:
            file.write(f"{self.username}|{self.message}\n")

    @staticmethod
    def load_all() -> list:
        posts = []
        try:
            with open('forum.txt', 'r') as file:
                for line in file:
                    username, message = line.strip().split('|')
                    posts.append(ForumPost(username, message))
        except FileNotFoundError:
            pass
        return posts