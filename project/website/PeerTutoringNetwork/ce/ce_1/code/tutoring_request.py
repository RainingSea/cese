class TutoringRequest:
    def __init__(self, subject: str, details: str, preferred_date: str):
        self.subject = subject
        self.details = details
        self.preferred_date = preferred_date

    def save(self):
        with open('tutoring_requests.txt', 'a') as f:
            f.write(f"{self.subject}|{self.details}|{self.preferred_date}\n")