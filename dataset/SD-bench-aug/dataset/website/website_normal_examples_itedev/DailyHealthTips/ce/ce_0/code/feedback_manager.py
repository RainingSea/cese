class FeedbackManager:
    def __init__(self, feedback_file: str):
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

    def submit_feedback(self, user: str, feedback: str) -> None:
        with open(self.feedback_file, 'a') as file:
            file.write(f"{user}|{feedback}\n")
        self.feedback.append(feedback)

    def get_feedback(self) -> list:
        return self.feedback