class FeedbackManager:
    def __init__(self, filename: str):
        self.filename = filename

    def submit_feedback(self, feedback: str) -> None:
        with open(self.filename, 'a') as file:
            file.write(f"{feedback}\n")