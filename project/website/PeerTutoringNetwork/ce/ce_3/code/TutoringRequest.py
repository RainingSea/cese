class TutoringRequest:
    def __init__(self, subject: str, details: str, preferred_date: str) -> None:
        self.subject = subject
        self.details = details
        self.preferred_date = preferred_date

    def save(self) -> None:
        pass  # Saving is handled by FileManager