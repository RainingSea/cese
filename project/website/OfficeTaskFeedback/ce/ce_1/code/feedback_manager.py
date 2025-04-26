class FeedbackManager:
    def __init__(self):
        self.feedbacks = self.load_feedbacks()

    def load_feedbacks(self):
        feedbacks = []
        try:
            with open('feedback.txt', 'r') as file:
                for line in file:
                    feedbacks.append(line.strip().split('|'))
        except FileNotFoundError:
            pass
        return feedbacks

    def submit_feedback(self, user: str, feedback: str, category: str) -> bool:
        self.feedbacks.append([user, feedback, category, 'Pending'])
        with open('feedback.txt', 'a') as file:
            file.write(f"{user}|{feedback}|{category}|Pending\n")
        return True

    def get_feedback_status(self, user: str) -> list:
        return [feedback for feedback in self.feedbacks if feedback[0] == user]