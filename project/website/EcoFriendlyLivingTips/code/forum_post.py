class ForumPost:
    """Represents a post in the community forum."""
    def __init__(self, username: str, content: str):
        self.username = username
        self.content = content

    def save(self):
        """Saves the forum post to a file."""
        with open('forum_posts.txt', 'a') as file:
            file.write(f"{self.username}|{self.content}\n")

    @staticmethod
    def load_all():
        """Loads all forum posts from the file."""
        forum_posts = []
        with open('forum_posts.txt', 'r') as file:
            for line in file:
                username, content = line.strip().split('|')
                forum_posts.append(ForumPost(username, content))
        return forum_posts