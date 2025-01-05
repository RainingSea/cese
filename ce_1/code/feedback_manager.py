class FeedbackManager:
    def __init__(self):
        self.feedback = []
        self.load_feedback()

    def submit_feedback(self, feedback: str) -> None:
        self.feedback.append(feedback)
        self.save_feedback()

    def load_feedback(self) -> None:
        try:
            with open('feedback.txt', 'r') as file:
                self.feedback = [line.strip() for line in file]
        except FileNotFoundError:
            pass

    def save_feedback(self) -> None:
        with open('feedback.txt', 'w') as file:
            for feedback_entry in self.feedback:
                file.write(f"{feedback_entry}\n")