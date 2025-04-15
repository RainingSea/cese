class Interaction:
    def __init__(self, user: str, album_id: str):
        self.user = user
        self.album_id = album_id
        self.likes = []
        self.comments = []

    @staticmethod
    def load_interactions() -> list:
        interactions = []
        try:
            with open('interactions.txt', 'r') as file:
                for line in file:
                    user, album_id, likes, comments = line.strip().split('|')
                    interaction = Interaction(user, album_id)
                    interaction.likes = likes.split(',') if likes else []
                    interaction.comments = comments.split(',') if comments else []
                    interactions.append(interaction)
        except FileNotFoundError:
            pass
        return interactions

    def like(self):
        if self.album_id not in self.likes:
            self.likes.append(self.album_id)

    def comment(self, comment: str):
        self.comments.append(comment)

    def follow(self, user: str):
        # Implement follow logic
        pass