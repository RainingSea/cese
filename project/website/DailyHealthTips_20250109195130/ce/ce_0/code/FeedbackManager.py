class FeedbackManager:
    def __init__(self):
        self.feedbacks = []
        self.load_feedbacks()

    def submit_feedback(self, feedback: str) -> None:
        self.feedbacks.append(feedback)
        self.save_feedbacks()

    def load_feedbacks(self) -> None:
        try:
            with open('feedback.txt', 'r') as file:
                self.feedbacks = [line.strip() for line in file]
        except FileNotFoundError:
            pass

    def save_feedbacks(self) -> None:
        with open('feedback.txt', 'w') as file:
            for feedback in self.feedbacks:
                file.write(f"{feedback}\n")