class FeedbackManager:
    def __init__(self, feedback_file):
        self.feedback_file = feedback_file
        self.load_feedback()

    def load_feedback(self):
        self.feedback = []
        try:
            with open(self.feedback_file, 'r') as file:
                for line in file:
                    self.feedback.append(line.strip())
        except FileNotFoundError:
            pass

    def submit_feedback(self, feedback: str) -> None:
        self.feedback.append(feedback)
        with open(self.feedback_file, 'a') as file:
            file.write(f"{feedback}\n")

    def get_all_feedback(self) -> list:
        return self.feedback