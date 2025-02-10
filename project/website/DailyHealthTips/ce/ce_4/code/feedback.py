class Feedback:
    def __init__(self, username: str, message: str) -> None:
        self.username = username
        self.message = message

    def save(self) -> None:
        with open('feedback.txt', 'a') as file:
            file.write(f'{self.username}|{self.message}\n')