class Feedback:
    def __init__(self, username: str, message: str):
        self.username = username
        self.message = message

    def save(self) -> None:
        with open('feedback.txt', 'a') as file:
            file.write(f"{self.username}|{self.message}\n")

    @staticmethod
    def load_all() -> list:
        feedbacks = []
        try:
            with open('feedback.txt', 'r') as file:
                for line in file:
                    username, message = line.strip().split('|')
                    feedbacks.append(Feedback(username, message))
        except FileNotFoundError:
            return feedbacks
        return feedbacks