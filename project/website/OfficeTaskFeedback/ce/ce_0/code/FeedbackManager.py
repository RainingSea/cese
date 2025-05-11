class FeedbackManager:
    def __init__(self):
        self.feedbacks = self.load_feedbacks()

    def load_feedbacks(self):
        feedbacks = []
        try:
            with open('feedback.txt', 'r') as file:
                for line in file:
                    feedback_id, user_id, content, category = line.strip().split('|')
                    feedbacks.append((feedback_id, user_id, content, category))
        except FileNotFoundError:
            pass
        return feedbacks

    def submit_feedback(self, user_id: str, content: str, category: str) -> bool:
        feedback_id = str(len(self.feedbacks) + 1)
        self.feedbacks.append((feedback_id, user_id, content, category))
        with open('feedback.txt', 'a') as file:
            file.write(f"{feedback_id}|{user_id}|{content}|{category}\n")
        return True

    def review_feedback(self) -> list:
        return self.feedbacks

    def get_feedback_status(self, user_id: str) -> list:
        return [feedback for feedback in self.feedbacks if feedback[1] == user_id]