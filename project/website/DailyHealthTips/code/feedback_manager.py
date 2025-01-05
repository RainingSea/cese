class FeedbackManager:
    def __init__(self, filename: str):
        self.filename = filename
        self.feedbacks = self.load_feedback()

    def submit_feedback(self, feedback: str) -> None:
        self.feedbacks.append(feedback)
        self.save_feedback()

    def load_feedback(self) -> list:
        feedbacks = []
        try:
            with open(self.filename, 'r') as file:
                for line in file:
                    feedbacks.append(line.strip())
        except FileNotFoundError:
            pass
        return feedbacks

    def save_feedback(self) -> None:
        with open(self.filename, 'w') as file:
            for feedback in self.feedbacks:
                file.write(f"{feedback}\n")