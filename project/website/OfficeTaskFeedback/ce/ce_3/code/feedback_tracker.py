from user import User
from feedback import Feedback

class FeedbackTracker:
    def __init__(self, users_file: str, feedback_file: str):
        self.users_file = users_file
        self.feedback_file = feedback_file
        self.load_users()

    def load_users(self):
        self.users = {}
        with open(self.users_file, 'r') as file:
            for line in file:
                username, password = line.strip().split('|')
                self.users[username] = password

    def register(self, username: str, password: str) -> bool:
        if username in self.users:
            return False
        user = User(username, password)
        user.save()
        self.users[username] = password
        return True

    def login(self, username: str, password: str) -> bool:
        return self.users.get(username) == password

    def submit_feedback(self, user: str, content: str, category: str) -> None:
        feedback = Feedback(user, content, category)
        feedback.save()

    def get_feedback(self, user: str) -> list:
        feedbacks = []
        with open(self.feedback_file, 'r') as file:
            for line in file:
                f_user, content, category, status = line.strip().split('|')
                if f_user == user:
                    feedbacks.append({
                        'content': content,
                        'category': category,
                        'status': status
                    })
        return feedbacks

    def get_all_feedback(self) -> list:
        feedbacks = []
        with open(self.feedback_file, 'r') as file:
            for line in file:
                f_user, content, category, status = line.strip().split('|')
                feedbacks.append({
                    'user': f_user,
                    'content': content,
                    'category': category,
                    'status': status
                })
        return feedbacks