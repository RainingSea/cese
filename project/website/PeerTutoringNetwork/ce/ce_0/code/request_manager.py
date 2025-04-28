class TutoringRequest:
    def __init__(self, request_id, subject, details, date):
        self.id = request_id
        self.subject = subject
        self.details = details
        self.date = date

class TutoringRequestManager:
    def __init__(self, filename):
        self.filename = filename
        self.requests = self.load_requests()

    def load_requests(self):
        requests = []
        try:
            with open(self.filename, 'r') as file:
                for line in file:
                    request_id, subject, details, date = line.strip().split('|')
                    requests.append(TutoringRequest(int(request_id), subject, details, date))
        except FileNotFoundError:
            pass
        return requests

    def create_request(self, subject: str, details: str, date: str) -> bool:
        request_id = len(self.requests) + 1
        new_request = TutoringRequest(request_id, subject, details, date)
        self.requests.append(new_request)
        self.save_requests()
        return True

    def cancel_request(self, request_id: int) -> bool:
        for request in self.requests:
            if request.id == request_id:
                self.requests.remove(request)
                self.save_requests()
                return True
        return False

    def get_requests(self):
        return self.requests

    def save_requests(self):
        with open(self.filename, 'w') as file:
            for request in self.requests:
                file.write(f"{request.id}|{request.subject}|{request.details}|{request.date}\n")