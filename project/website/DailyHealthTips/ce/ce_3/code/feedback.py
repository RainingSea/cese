class Feedback:
    def __init__(self, username: str, comment: str):
        self.username = username
        self.comment = comment

    def save(self):
        with open('feedback.txt', 'a') as f:
            f.write(f"{self.username}|{self.comment}\n")

    @staticmethod
    def load_all() -> list:
        feedbacks = []
        with open('feedback.txt', 'r') as f:
            for line in f:
                username, comment = line.strip().split('|')
                feedbacks.append(Feedback(username, comment))
        return feedbacks