import datetime

class FeedbackManager:
    def __init__(self, feedback_file='feedback.txt'):
        self.feedback_file = feedback_file
        self._ensure_feedback_exists()

    def _ensure_feedback_exists(self):
        try:
            with open(self.feedback_file, 'r') as f:
                pass
        except FileNotFoundError:
            with open(self.feedback_file, 'w') as f:
                f.write("")

    def submit_feedback(self, username, tip_id, comment):
        if not self._validate_feedback(username, tip_id, comment):
            return False
        
        timestamp = datetime.datetime.now().isoformat()
        with open(self.feedback_file, 'a') as f:
            f.write(f"{username}|{tip_id}|{timestamp}|{comment}\n")
        return True

    def get_feedback(self):
        with open(self.feedback_file, 'r') as f:
            return [line.strip().split('|', 3) for line in f.readlines()]

    def _validate_feedback(self, username, tip_id, comment):
        return bool(username and tip_id and comment)