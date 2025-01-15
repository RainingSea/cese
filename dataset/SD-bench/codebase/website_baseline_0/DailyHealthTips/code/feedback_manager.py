class FeedbackManager:
    def __init__(self):
        self.feedback = []

    def load_feedback(self):
        try:
            with open('feedback.txt', 'r') as file:
                self.feedback = [line.strip() for line in file]
        except FileNotFoundError:
            print("Feedback data file not found. Starting with an empty feedback list.")

    def submit_feedback(self, user: str, feedback: str) -> None:
        self.feedback.append(f"{user}|{feedback}")
        with open('feedback.txt', 'a') as file:
            file.write(f"{user}|{feedback}\n")