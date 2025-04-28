class Feedback:
    def __init__(self, username: str, feedback: str, category: str):
        self.username = username
        self.feedback = feedback
        self.category = category
        self.status = 'Submitted'

class FeedbackManager:
    def __init__(self, filename: str):
        self.filename = filename
        self.feedback_list = self.load_feedback()

    def load_feedback(self):
        feedbacks = []
        try:
            with open(self.filename, 'r') as file:
                for line in file:
                    username, feedback, category, status = line.strip().split('|')
                    feedback_entry = Feedback(username, feedback, category)
                    feedback_entry.status = status
                    feedbacks.append(feedback_entry)
        except FileNotFoundError:
            pass
        return feedbacks

    def submit_feedback(self, username: str, feedback: str, category: str) -> bool:
        new_feedback = Feedback(username, feedback, category)
        self.feedback_list.append(new_feedback)
        with open(self.filename, 'a') as file:
            file.write(f"{username}|{feedback}|{category}|{new_feedback.status}\n")
        return True

    def get_feedback_status(self, username: str) -> list:
        return [feedback for feedback in self.feedback_list if feedback.username == username]