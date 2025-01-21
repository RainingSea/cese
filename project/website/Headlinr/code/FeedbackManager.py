import os

class FeedbackManager:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.feedback = self.load_feedback()

    def load_feedback(self) -> list:
        if not os.path.exists(self.file_path):
            return []
        with open(self.file_path, 'r') as file:
            return [line.strip() for line in file.readlines()]

    def save_feedback(self) -> None:
        with open(self.file_path, 'w') as file:
            for feedback in self.feedback:
                file.write(f"{feedback}\n")

    def submit_feedback(self, user: str, feedback: str) -> None:
        self.feedback.append(f"{user}: {feedback}")
        self.save_feedback()

    def get_feedback(self) -> list:
        return self.feedback