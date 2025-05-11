class FeedbackManager:
    def __init__(self):
        self.feedbacks = self.load_feedbacks()

    def load_feedbacks(self):
        feedbacks = []
        try:
            with open('feedback.txt', 'r') as file:
                for line in file:
                    username, feedback_text, category, status = line.strip().split('|')
                    feedbacks.append([username, feedback_text, category, status])
        except FileNotFoundError:
            pass
        return feedbacks

    def submit_feedback(self, username: str, feedback: str, category: str) -> None:
        self.feedbacks.append([username, feedback, category, 'Pending'])
        with open('feedback.txt', 'a') as file:
            file.write(f"{username}|{feedback}|{category}|Pending\n")

    def get_feedbacks(self) -> list:
        return self.feedbacks

    def get_feedback_status(self, username: str) -> list:
        return [f for f in self.feedbacks if f[0] == username]