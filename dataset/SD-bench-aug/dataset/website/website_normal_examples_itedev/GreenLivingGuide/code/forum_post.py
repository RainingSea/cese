class ForumPost:
    def __init__(self, username: str, content: str) -> None:
        self.username = username
        self.content = content

    def save(self) -> None:
        with open('forum_posts.txt', 'a') as file:
            file.write(f"{self.username}|{self.content}\n")

    @staticmethod
    def load_posts() -> list:
        posts = []
        try:
            with open('forum_posts.txt', 'r') as file:
                for line in file:
                    username, content = line.strip().split('|')
                    posts.append((username, content))
        except FileNotFoundError:
            pass
        return posts