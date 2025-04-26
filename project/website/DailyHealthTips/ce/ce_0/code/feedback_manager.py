class FeedbackManager:
    def __init__(self):
        self.feedbacks = self.load_feedbacks()

    def load_feedbacks(self):
        feedbacks = []
        try:
            with open('feedback.txt', 'r') as file:
                for line in file:
                    username, feedback = line.strip().split(':', 1)
                    feedbacks.append((username, feedback))
        except FileNotFoundError:
            pass
        return feedbacks

    def submit_feedback(self, username: str, feedback: str) -> None:
        self.feedbacks.append((username, feedback))
        with open('feedback.txt', 'a') as file:
            file.write(f"{username}:{feedback}\n")