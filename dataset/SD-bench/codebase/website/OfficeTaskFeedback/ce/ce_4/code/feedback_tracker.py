from user import User
from feedback import Feedback

class FeedbackTracker:
    def register_user(self, username: str, password: str) -> bool:
        user = User(username, password)
        user.save()
        return True

    def login_user(self, username: str, password: str) -> bool:
        user = User(username, password)
        return user.validate()

    def submit_feedback(self, user: str, content: str, category: str) -> None:
        feedback = Feedback(user, content, category)
        feedback.save()

    def get_feedback_status(self, user: str) -> list:
        with open('feedback.txt', 'r') as file:
            feedbacks = file.readlines()
            return [feedback.strip().split('|') for feedback in feedbacks if feedback.strip().split('|')[0] == user]

    def review_feedback(self) -> list:
        with open('feedback.txt', 'r') as file:
            return [feedback.strip().split('|') for feedback in file.readlines()]