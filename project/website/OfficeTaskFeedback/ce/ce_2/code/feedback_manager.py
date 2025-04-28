class FeedbackManager:
    def __init__(self):
        self.feedbacks = self.load_feedbacks()

    def load_feedbacks(self):
        feedbacks = []
        try:
            with open('feedback.txt', 'r') as file:
                for line in file:
                    feedbacks.append(line.strip())
        except FileNotFoundError:
            pass
        return feedbacks

    def submit_feedback(self, username: str, feedback: str, category: str) -> bool:
        feedback_entry = f"{username}|{feedback}|{category}"
        self.feedbacks.append(feedback_entry)
        with open('feedback.txt', 'a') as file:
            file.write(f"{feedback_entry}\n")
        return True

    def get_feedbacks(self):
        return self.feedbacks