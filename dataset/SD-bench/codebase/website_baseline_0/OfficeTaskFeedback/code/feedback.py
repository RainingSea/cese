class Feedback:
    def __init__(self):
        self.feedback_file = 'feedback.txt'
        self.load_feedback()

    def load_feedback(self):
        self.feedback_entries = []
        try:
            with open(self.feedback_file, 'r') as file:
                for line in file:
                    username, feedback_text, category, status = line.strip().split('|')
                    self.feedback_entries.append({
                        'username': username,
                        'feedback_text': feedback_text,
                        'category': category,
                        'status': status
                    })
        except FileNotFoundError:
            self.feedback_entries = []

    def submit_feedback(self, username: str, feedback_text: str, category: str) -> bool:
        status = 'Pending'
        with open(self.feedback_file, 'a') as file:
            file.write(f"{username}|{feedback_text}|{category}|{status}\n")
        self.feedback_entries.append({
            'username': username,
            'feedback_text': feedback_text,
            'category': category,
            'status': status
        })
        return True

    def review_feedback(self) -> list:
        return self.feedback_entries