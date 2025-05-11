class FeedbackManager:
    def __init__(self, feedback_file: str):
        self.feedback_file = feedback_file
        self.load_feedback()

    def load_feedback(self):
        """Load feedback from the specified file."""
        self.feedback = []
        try:
            with open(self.feedback_file, 'r') as file:
                for line in file:
                    username, feedback, category = line.strip().split('|')
                    self.feedback.append({
                        'username': username,
                        'feedback': feedback,
                        'category': category
                    })
        except FileNotFoundError:
            pass

    def submit(self, feedback: str, category: str, username: str) -> None:
        """Submit feedback from the logged-in user."""
        if username is None:
            raise ValueError("User must be logged in to submit feedback.")
        self.feedback.append({'username': username, 'feedback': feedback, 'category': category})
        with open(self.feedback_file, 'a') as file:
            file.write(f"{username}|{feedback}|{category}\n")

    def get_status(self, username: str) -> str:
        """Get the status of feedback submitted by the user."""
        user_feedback = [f"{f['feedback']} ({f['category']})" for f in self.feedback if f['username'] == username]
        return "\n".join(user_feedback) if user_feedback else "No feedback submitted."

    def review(self) -> list:
        """Review all feedback."""
        return self.feedback

    def get_feedbacks(self) -> list:
        """Get all feedbacks."""
        return self.feedback