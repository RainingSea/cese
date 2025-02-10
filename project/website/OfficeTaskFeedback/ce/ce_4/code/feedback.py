class Feedback:
    def __init__(self, user: str, content: str, category: str):
        self.user = user
        self.content = content
        self.category = category
        self.status = 'Pending'

    def save(self) -> None:
        with open('feedback.txt', 'a') as file:
            file.write(f"{self.user}|{self.content}|{self.category}|{self.status}\n")