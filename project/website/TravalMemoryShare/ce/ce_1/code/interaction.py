class Interaction:
    def __init__(self, user_id: str, album_id: str, type: str):
        self.user_id = user_id
        self.album_id = album_id
        self.type = type

    def save(self):
        with open('interactions.txt', 'a') as f:
            f.write(f"{self.user_id}|{self.album_id}|{self.type}\n")