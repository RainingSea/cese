class Comment:
    def __init__(self, user: str, album_id: str, content: str):
        self.user = user
        self.album_id = album_id
        self.content = content

    def add_comment(self) -> bool:
        with open('comments.txt', 'a') as file:
            file.write(f"{self.user}|{self.album_id}|{self.content}\n")
        return True