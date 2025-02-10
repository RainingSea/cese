from user import User
from thread import Thread
from contact_inquiry import ContactInquiry

class FileManager:
    def save_user(self, user: User) -> None:
        user.save()

    def load_users(self) -> list:
        users = []
        try:
            with open('users.txt', 'r') as f:
                for line in f:
                    username, password = line.strip().split('|')
                    users.append(User(username, password))
        except FileNotFoundError:
            pass
        return users

    def save_thread(self, thread: Thread) -> None:
        thread.save()

    def load_threads(self) -> list:
        threads = []
        try:
            with open('threads.txt', 'r') as f:
                for line in f:
                    title, content, *comments = line.strip().split('|')
                    thread = Thread(title, content)
                    thread.comments = comments
                    threads.append(thread)
        except FileNotFoundError:
            pass
        return threads

    def save_contact_inquiry(self, inquiry: ContactInquiry) -> None:
        inquiry.save()

    def load_contact_inquiries(self) -> list:
        inquiries = []
        try:
            with open('contact_inquiries.txt', 'r') as f:
                for line in f:
                    name, email, message = line.strip().split('|')
                    inquiries.append(ContactInquiry(name, email, message))
        except FileNotFoundError:
            pass
        return inquiries