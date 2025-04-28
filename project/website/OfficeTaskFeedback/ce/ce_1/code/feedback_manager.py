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

    def submit_feedback(self, username: str, category: str, feedback: str) -> bool:
        self.feedbacks.append([username, category, feedback])
        with open('feedback.txt', 'a') as file:
            file.write(f"{username}|{category}|{feedback}\n")
        return True

    def get_feedbacks(self) -> list:
        return self.feedbacks