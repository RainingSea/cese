class Feedback:
    def __init__(self, username: str, message: str):
        self.username = username
        self.message = message

    def save(self) -> None:
        """Save the feedback to the feedback.txt file."""
        with open('feedback.txt', 'a') as file:
            file.write(f"{self.username}|{self.message}\n")