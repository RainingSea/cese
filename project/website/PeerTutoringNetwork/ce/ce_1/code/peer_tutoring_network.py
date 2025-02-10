from user import User
from tutoring_request import TutoringRequest
from contact_message import ContactMessage

class PeerTutoringNetwork:
    def __init__(self):
        self.users = []
        self.tutoring_requests = []
        self.contact_messages = []

    def register_user(self, username: str, password: str, email: str):
        user = User(username, password, email)
        user.save()
        self.users.append(user)

    def login(self, username: str, password: str) -> bool:
        for user in self.users:
            if user.username == username and user.password == password:
                return True
        return False

    def request_tutoring(self, subject: str, details: str, preferred_date: str):
        request = TutoringRequest(subject, details, preferred_date)
        request.save()
        self.tutoring_requests.append(request)

    def contact_support(self, name: str, email: str, message: str):
        contact_message = ContactMessage(name, email, message)
        contact_message.save()
        self.contact_messages.append(contact_message)

    def load_users(self):
        try:
            with open('users.txt', 'r') as f:
                for line in f:
                    username, password, email = line.strip().split('|')
                    self.users.append(User(username, password, email))
        except FileNotFoundError:
            pass

    def load_tutoring_requests(self):
        try:
            with open('tutoring_requests.txt', 'r') as f:
                for line in f:
                    subject, details, preferred_date = line.strip().split('|')
                    self.tutoring_requests.append(TutoringRequest(subject, details, preferred_date))
        except FileNotFoundError:
            pass

    def load_contact_messages(self):
        try:
            with open('contact_messages.txt', 'r') as f:
                for line in f:
                    name, email, message = line.strip().split('|')
                    self.contact_messages.append(ContactMessage(name, email, message))
        except FileNotFoundError:
            pass

    def get_user(self, username: str):
        for user in self.users:
            if user.username == username:
                return user
        return None