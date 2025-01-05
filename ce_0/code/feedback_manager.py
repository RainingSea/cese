class FeedbackManager:
    def __init__(self):
        self.feedback = []

    def submit_feedback(self, feedback: str) -> None:
        self.feedback.append(feedback)
        self.save_feedback()

    def load_feedback(self) -> None:
        try:
            with open('feedback.txt', 'r') as f:
                self.feedback = [line.strip() for line in f.readlines()]
        except FileNotFoundError:
            pass

    def save_feedback(self) -> None:
        with open('feedback.txt', 'w') as f:
            for feedback in self.feedback:
                f.write(f"{feedback}\n")