class FeedbackManager:
    def __init__(self, filename: str):
        self.filename = filename
        self.feedback_list = self.load_feedback()

    def submit_feedback(self, feedback: str):
        self.feedback_list.append(feedback)
        self.save_feedback()

    def load_feedback(self) -> list:
        feedback = []
        with open(self.filename, 'r') as file:
            for line in file:
                if line.strip():
                    feedback.append(line.strip())
        return feedback

    def save_feedback(self):
        with open(self.filename, 'w') as file:
            for feedback in self.feedback_list:
                file.write(feedback + "\n")