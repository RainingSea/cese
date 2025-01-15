class Feedback:
    def __init__(self, user: str, content: str, category: str):
        """Initialize Feedback with user, content, category, and default status."""
        self.user = user
        self.content = content
        self.category = category
        self.status = 'Pending'

    def save(self) -> None:
        """Save the feedback to the feedback.txt file."""
        with open('feedback.txt', 'a') as file:
            file.write(f"{self.user}|{self.content}|{self.category}|{self.status}\n")

    @staticmethod
    def load_all() -> list:
        """Load all feedback from the feedback.txt file."""
        feedbacks = []
        try:
            with open('feedback.txt', 'r') as file:
                for line in file:
                    user, content, category, status = line.strip().split('|')
                    feedback = Feedback(user, content, category)
                    feedback.status = status
                    feedbacks.append(feedback)
        except FileNotFoundError:
            pass
        return feedbacks