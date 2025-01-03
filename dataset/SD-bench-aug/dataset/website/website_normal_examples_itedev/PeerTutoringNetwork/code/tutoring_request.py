class TutoringRequest:
    def __init__(self, username: str, subject: str, details: str, preferred_date: str):
        self.username = username
        self.subject = subject
        self.details = details
        self.preferred_date = preferred_date

    def save(self):
        pass  # Saving is handled in main.py