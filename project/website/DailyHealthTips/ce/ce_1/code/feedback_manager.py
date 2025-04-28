class FeedbackManager:
    def __init__(self):
        self.feedbacks = self.load_feedbacks()

    def load_feedbacks(self):
        feedbacks = []
        with open('feedback.txt', 'r') as file:
            for line in file:
                feedbacks.append(line.strip())
        return feedbacks

    def submit_feedback(self, feedback: str) -> None:
        self.feedbacks.append(feedback)
        with open('feedback.txt', 'a') as file:
            file.write(f"{feedback}\n")