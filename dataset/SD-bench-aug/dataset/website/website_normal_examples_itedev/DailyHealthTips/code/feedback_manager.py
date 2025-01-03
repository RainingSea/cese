class FeedbackManager:
    def __init__(self, feedback_file: str):
        self.feedback_file = feedback_file
        self.feedbacks = self.load_feedback()

    def load_feedback(self) -> list:
        feedbacks = []
        try:
            with open(self.feedback_file, 'r') as file:
                for line in file:
                    if line.strip():  # Avoid empty lines
                        feedbacks.append(line.strip())
        except FileNotFoundError:
            with open(self.feedback_file, 'w'):  # Create file if not exists
                pass
        return feedbacks

    def submit_feedback(self, user: str, feedback: str) -> None:
        with open(self.feedback_file, 'a') as file:
            file.write(f"{user}|{feedback}\n")
        self.feedbacks.append(f"{user}|{feedback}")  # Update in-memory list