class FeedbackManager:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def submit_feedback(self, feedback: str) -> None:
        with open(self.file_path, 'a') as file:
            file.write(f"{feedback}\n")