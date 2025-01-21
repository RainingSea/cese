class FeedbackManager:
    def __init__(self, filename: str):
        self.filename = filename
        self.feedback_list = self.load_feedback()

    def submit_feedback(self, feedback: str) -> bool:
        """Submits feedback and saves it to the file."""
        with open(self.filename, 'a') as file:
            file.write(f"{feedback}\n")
        self.feedback_list.append(feedback)
        return True

    def load_feedback(self) -> list:
        """Loads feedback from the specified file."""
        feedback_list = []
        try:
            with open(self.filename, 'r') as file:
                feedback_list = [line.strip() for line in file]
        except FileNotFoundError:
            pass
        return feedback_list