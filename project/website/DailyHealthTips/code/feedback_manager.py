class FeedbackManager:
    def __init__(self, feedback_file: str):
        self.feedback_file = feedback_file
        self.feedbacks = self.load_feedback()

    def load_feedback(self) -> list:
        feedbacks = []
        try:
            with open(self.feedback_file, 'r') as file:
                for line in file:
                    feedbacks.append(line.strip())
        except FileNotFoundError:
            open(self.feedback_file, 'w').close()  # Create file if it doesn't exist
        return feedbacks

    def submit_feedback(self, feedback: str) -> bool:
        with open(self.feedback_file, 'a') as file:
            file.write(f"{feedback}\n")
        self.feedbacks.append(feedback)
        return True

    def get_all_feedback(self) -> list:
        return self.feedbacks