class FeedbackManager:
    def __init__(self):
        self.feedbacks = self.load_feedbacks()

    def load_feedbacks(self):
        feedbacks = []
        with open('feedback.txt', 'r') as file:
            for line in file:
                username, feedback, category = line.strip().split('|')
                feedbacks.append((username, feedback, category))
        return feedbacks

    def submit_feedback(self, username: str, feedback: str, category: str) -> bool:
        self.feedbacks.append((username, feedback, category))
        with open('feedback.txt', 'a') as file:
            file.write(f"{username}|{feedback}|{category}\n")
        return True

    def review_feedback(self):
        return self.feedbacks