class FeedbackManager:
    def __init__(self, feedback_file):
        self.feedback_file = feedback_file
        self.feedbacks = self.load_feedback()

    def submit_feedback(self, feedback: str) -> None:
        self.feedbacks.append(feedback)
        self.save_feedback()

    def load_feedback(self) -> list:
        feedbacks = []
        try:
            with open(self.feedback_file, 'r') as file:
                for line in file:
                    feedbacks.append(line.strip())
        except FileNotFoundError:
            pass
        return feedbacks

    def save_feedback(self) -> None:
        with open(self.feedback_file, 'w') as file:
            for feedback in self.feedbacks:
                file.write(f"{feedback}\n")