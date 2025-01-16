class TutoringRequest:
    def __init__(self, subject: str, details: str, preferred_date: str, username: str):
        self.subject = subject
        self.details = details
        self.preferred_date = preferred_date
        self.username = username

    def save(self):
        pass  # Not used in this implementation