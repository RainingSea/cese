class FeedbackManager:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.feedbacks = self.load_feedback()

    def load_feedback(self) -> list:
        try:
            with open(self.file_path, 'r') as file:
                return [line.strip() for line in file.readlines()]
        except FileNotFoundError:
            return []

    def submit_feedback(self, feedback: str) -> None:
        self.feedbacks.append(feedback)
        self._save_feedback()

    def get_feedback(self) -> list:
        return self.feedbacks

    def _save_feedback(self) -> None:
        with open(self.file_path, 'w') as file:
            for feedback in self.feedbacks:
                file.write(feedback + '\n')