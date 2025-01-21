class FeedbackManager:
    def __init__(self, feedback_file: str):
        self.feedback_file = feedback_file
        self.feedbacks = self.load_feedback()

    def load_feedback(self) -> list:
        with open(self.feedback_file, 'r') as file:
            return [line.strip() for line in file]

    def submit_feedback(self, feedback: str) -> None:
        with open(self.feedback_file, 'a') as file:
            file.write(f"{feedback}\n")
        self.feedbacks.append(feedback)

    def get_all_feedback(self) -> list:
        return self.feedbacks