class FeedbackManager:
    def __init__(self):
        self.feedbacks = self.load_feedbacks()

    def load_feedbacks(self):
        feedbacks = []
        try:
            with open('feedback.txt', 'r') as file:
                for line in file:
                    user_id, category, content = line.strip().split('|')
                    feedbacks.append({'user_id': user_id, 'category': category, 'content': content})
        except FileNotFoundError:
            pass
        return feedbacks

    def submit_feedback(self, user_id: str, category: str, content: str) -> bool:
        self.feedbacks.append({'user_id': user_id, 'category': category, 'content': content})
        self.save_feedbacks()
        return True

    def save_feedbacks(self):
        with open('feedback.txt', 'w') as file:
            for feedback in self.feedbacks:
                file.write(f"{feedback['user_id']}|{feedback['category']}|{feedback['content']}\n")

    def review_feedback(self) -> list:
        return self.feedbacks

    def get_feedback_status(self, user_id: str) -> list:
        return [feedback for feedback in self.feedbacks if feedback['user_id'] == user_id]