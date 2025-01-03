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
            # If the file does not exist, initialize with an empty list
            self.feedback = []

    def submit_feedback(self, feedback: str) -> None:
        with open(self.feedback_file, 'a') as file:
            file.write(f"{feedback}\n")
        self.feedback.append(feedback)

    def get_all_feedback(self) -> list:
        return self.feedback