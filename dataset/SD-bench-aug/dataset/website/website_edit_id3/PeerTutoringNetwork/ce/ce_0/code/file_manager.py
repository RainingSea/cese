from user import User
from tutor import Tutor
from tutoring_request import TutoringRequest

class FileManager:
    def save_user(self, user: User):
        with open('users.txt', 'a') as f:
            f.write(f"{user.username}|{user.password}|{user.email}\n")

    def load_users(self) -> list[User]:
        users = []
        with open('users.txt', 'r') as f:
            for line in f:
                username, password, email = line.strip().split('|')
                users.append(User(username, password, email))
        return users

    def save_tutoring_request(self, request: TutoringRequest):
        with open('tutoring_requests.txt', 'a') as f:
            f.write(f"{request.subject}|{request.details}|{request.preferred_date}|{request.username}\n")

    def load_tutoring_requests(self) -> list[TutoringRequest]:
        requests = []
        with open('tutoring_requests.txt', 'r') as f:
            for line in f:
                subject, details, preferred_date, username = line.strip().split('|')
                requests.append(TutoringRequest(subject, details, preferred_date, username))
        return requests

    def load_tutors(self) -> list[Tutor]:
        tutors = []
        with open('tutors.txt', 'r') as f:
            for line in f:
                name, subject = line.strip().split('|')
                tutors.append(Tutor(name, subject))
        return tutors