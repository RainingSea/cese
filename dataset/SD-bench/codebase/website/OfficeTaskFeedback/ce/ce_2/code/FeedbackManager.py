class FeedbackManager:
    def __init__(self, feedback_file: str, status_file: str):
        self.feedback_file = feedback_file
        self.status_file = status_file
        self.feedbacks = self.load_feedback()
        self.statuses = self.load_status()

    def submit_feedback(self, username: str, feedback: str, category: str) -> bool:
        feedback_id = len(self.feedbacks) + 1
        self.feedbacks.append({
            'id': feedback_id,
            'username': username,
            'feedback': feedback,
            'category': category,
            'status': 'Pending'
        })
        self.save_feedback()
        self.update_status(feedback_id, 'Pending')
        return True

    def load_feedback(self) -> list:
        feedbacks = []
        try:
            with open(self.feedback_file, 'r') as file:
                for line in file:
                    feedback_data = line.strip().split('|')
                    feedbacks.append({
                        'id': int(feedback_data[0]),
                        'username': feedback_data[1],
                        'feedback': feedback_data[2],
                        'category': feedback_data[3],
                        'status': feedback_data[4]
                    })
        except FileNotFoundError:
            pass
        return feedbacks

    def update_status(self, feedback_id: int, status: str) -> bool:
        for feedback in self.feedbacks:
            if feedback['id'] == feedback_id:
                feedback['status'] = status
                self.save_status()
                return True
        return False

    def load_status(self) -> dict:
        statuses = {}
        try:
            with open(self.status_file, 'r') as file:
                for line in file:
                    feedback_id, status = line.strip().split('|')
                    statuses[int(feedback_id)] = status
        except FileNotFoundError:
            pass
        return statuses

    def save_feedback(self):
        with open(self.feedback_file, 'w') as file:
            for feedback in self.feedbacks:
                file.write(f"{feedback['id']}|{feedback['username']}|{feedback['feedback']}|{feedback['category']}|{feedback['status']}\n")

    def save_status(self):
        with open(self.status_file, 'w') as file:
            for feedback in self.feedbacks:
                file.write(f"{feedback['id']}|{feedback['status']}\n")