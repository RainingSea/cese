class User:
    def __init__(self, username: str, password: str, email: str):
        self.username = username
        self.password = password
        self.email = email

    def to_string(self) -> str:
        return f"{self.username}|{self.password}|{self.email}"

class Tutor:
    def __init__(self, name: str, subject: str):
        self.name = name
        self.subject = subject

    def to_string(self) -> str:
        return f"{self.name}|{self.subject}"

class TutoringRequest:
    def __init__(self, subject: str, details: str, preferred_date: str, username: str):
        self.subject = subject
        self.details = details
        self.preferred_date = preferred_date
        self.username = username

    def to_string(self) -> str:
        return f"{self.subject}|{self.details}|{self.preferred_date}|{self.username}"

class FileManager:
    def save_user(self, user: User):
        with open('users.txt', 'a') as f:
            f.write(user.to_string() + "\n")

    def load_users(self) -> list[User]:
        users = []
        try:
            with open('users.txt', 'r') as f:
                for line in f:
                    username, password, email = line.strip().split('|')
                    users.append(User(username, password, email))
        except FileNotFoundError:
            pass
        return users

    def save_tutoring_request(self, request: TutoringRequest):
        with open('tutoring_requests.txt', 'a') as f:
            f.write(request.to_string() + "\n")

    def load_tutoring_requests(self) -> list[TutoringRequest]:
        requests = []
        try:
            with open('tutoring_requests.txt', 'r') as f:
                for line in f:
                    subject, details, preferred_date, username = line.strip().split('|')
                    requests.append(TutoringRequest(subject, details, preferred_date, username))
        except FileNotFoundError:
            pass
        return requests

    def load_tutors(self) -> list[Tutor]:
        tutors = []
        try:
            with open('tutors.txt', 'r') as f:
                for line in f:
                    name, subject = line.strip().split('|')
                    tutors.append(Tutor(name, subject))
        except FileNotFoundError:
            pass
        return tutors

    def cancel_tutoring_request(self, username: str, subject: str):
        requests = self.load_tutoring_requests()
        requests = [req for req in requests if not (req.username == username and req.subject == subject)]
        with open('tutoring_requests.txt', 'w') as f:
            for req in requests:
                f.write(req.to_string() + "\n")