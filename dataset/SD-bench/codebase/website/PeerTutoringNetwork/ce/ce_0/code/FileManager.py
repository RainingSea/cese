import os
from User import User
from Tutor import Tutor
from TutoringRequest import TutoringRequest
from SupportContact import SupportContact

class FileManager:
    def __init__(self):
        self.user_file = 'users.txt'
        self.tutor_file = 'tutors.txt'
        self.request_file = 'requests.txt'
        self.contact_file = 'support_contacts.txt'

    def save_user(self, user: User):
        with open(self.user_file, 'a') as f:
            f.write(user.to_string() + '\n')

    def load_users(self) -> list[User]:
        users = []
        if os.path.exists(self.user_file):
            with open(self.user_file, 'r') as f:
                for line in f:
                    username, password, email = line.strip().split('|')
                    users.append(User(username, password, email))
        return users

    def save_tutor(self, tutor: Tutor):
        with open(self.tutor_file, 'a') as f:
            f.write(tutor.to_string() + '\n')

    def load_tutors(self) -> list[Tutor]:
        tutors = []
        if os.path.exists(self.tutor_file):
            with open(self.tutor_file, 'r') as f:
                for line in f:
                    name, subject = line.strip().split('|')
                    tutors.append(Tutor(name, subject))
        return tutors

    def save_request(self, request: TutoringRequest):
        with open(self.request_file, 'a') as f:
            f.write(request.to_string() + '\n')

    def load_requests(self) -> list[TutoringRequest]:
        requests = []
        if os.path.exists(self.request_file):
            with open(self.request_file, 'r') as f:
                for line in f:
                    username, subject, details, preferred_date = line.strip().split('|')
                    requests.append(TutoringRequest(username, subject, details, preferred_date))
        return requests

    def save_contact(self, contact: SupportContact):
        with open(self.contact_file, 'a') as f:
            f.write(contact.to_string() + '\n')

    def load_contacts(self) -> list[SupportContact]:
        contacts = []
        if os.path.exists(self.contact_file):
            with open(self.contact_file, 'r') as f:
                for line in f:
                    name, email, message = line.strip().split('|')
                    contacts.append(SupportContact(name, email, message))
        return contacts