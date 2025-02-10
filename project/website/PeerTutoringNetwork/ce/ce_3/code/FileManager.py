import os
from User import User
from TutoringRequest import TutoringRequest
from Tutor import Tutor

class FileManager:
    def __init__(self):
        self.users_file = 'users.txt'
        self.requests_file = 'tutoring_requests.txt'
        self.tutors_file = 'tutors.txt'

    def save_user(self, user: User) -> None:
        with open(self.users_file, 'a') as file:
            file.write(f"{user.username}|{user.password}|{user.email}\n")

    def load_users(self) -> list[User]:
        users = []
        if os.path.exists(self.users_file):
            with open(self.users_file, 'r') as file:
                for line in file:
                    username, password, email = line.strip().split('|')
                    users.append(User(username, password, email))
        return users

    def save_request(self, request: TutoringRequest) -> None:
        with open(self.requests_file, 'a') as file:
            file.write(f"{request.subject}|{request.details}|{request.preferred_date}\n")

    def load_requests(self) -> list[TutoringRequest]:
        requests = []
        if os.path.exists(self.requests_file):
            with open(self.requests_file, 'r') as file:
                for line in file:
                    subject, details, preferred_date = line.strip().split('|')
                    requests.append(TutoringRequest(subject, details, preferred_date))
        return requests

    def load_tutors(self) -> list[Tutor]:
        tutors = []
        if os.path.exists(self.tutors_file):
            with open(self.tutors_file, 'r') as file:
                for line in file:
                    name, subject = line.strip().split('|')
                    tutors.append(Tutor(name, subject))
        return tutors