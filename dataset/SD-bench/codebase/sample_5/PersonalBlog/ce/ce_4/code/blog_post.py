class BlogPost:
    def __init__(self, username: str, post_id: int, title: str, content: str):
        self.username = username
        self.post_id = post_id
        self.title = title
        self.content = content

    def create_post(self, username: str, title: str, content: str) -> bool:
        # Assuming post creation is always successful for simplicity
        return True

    def edit_post(self, post_id: int, title: str, content: str) -> bool:
        self.title = title
        self.content = content
        return True

    def delete_post(self, post_id: int) -> bool:
        return True

    def get_post(self, post_id: int) -> str:
        return f"{self.title}: {self.content}"