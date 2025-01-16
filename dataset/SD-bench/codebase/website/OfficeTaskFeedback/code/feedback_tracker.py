from feedback import Feedback

class FeedbackTracker:
    def __init__(self):
        """Initialize FeedbackTracker and load existing feedback."""
        self.feedbacks = Feedback.load_all()

    def track_feedback(self, feedback: Feedback) -> None:
        """Track new feedback by adding it to the list."""
        self.feedbacks.append(feedback)

    def update_status(self, feedback_id: int, status: str) -> None:
        """Update the status of feedback by its ID."""
        if 0 <= feedback_id < len(self.feedbacks):
            self.feedbacks[feedback_id].status = status
            self.save_status()

    def get_status(self, user: str) -> list:
        """Get the status of feedback for a specific user."""
        return [feedback for feedback in self.feedbacks if feedback.user == user]

    def save_status(self) -> None:
        """Save the current feedback status to feedback_status.txt."""
        with open('feedback_status.txt', 'w') as file:
            for feedback in self.feedbacks:
                file.write(f"{feedback.user}|{feedback.content}|{feedback.category}|{feedback.status}\n")