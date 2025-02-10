class Feedback:
    def __init__(self, username: str, message: str):
        self.username = username
        self.message = message

    def save(self):
        with open('feedback.txt', 'a') as file:
            file.write(f"{self.username}|{self.message}\n")