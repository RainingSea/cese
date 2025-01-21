import os
from models import User, Thread, Comment, Advice, ContactInquiry

class DataStorage:
    def __init__(self):
        self.users_file = 'users.txt'
        self.threads_file = 'threads.txt'
        self.comments_file = 'comments.txt'
        self.advice_file = 'advice.txt'
        self.contact_inquiries_file = 'contact_inquiries.txt'

    def save_user(self, user: User):
        with open(self.users_file, 'a') as f:
            f.write(f"{user.username}|{user.password}\n")

    def load_users(self) -> list:
        users = []
        if os.path.exists(self.users_file):
            with open(self.users_file, 'r') as f:
                for line in f:
                    username, password = line.strip().split('|')
                    users.append(User(username, password))
        return users

    def save_thread(self, thread: Thread):
        with open(self.threads_file, 'a') as f:
            f.write(f"{thread.title}|{thread.content}\n")

    def load_threads(self) -> list:
        threads = []
        if os.path.exists(self.threads_file):
            with open(self.threads_file, 'r') as f:
                for line in f:
                    title, content = line.strip().split('|')
                    threads.append(Thread(title, content))
        return threads

    def save_comment(self, thread_title: str, comment: Comment):
        with open(self.comments_file, 'a') as f:
            f.write(f"{thread_title}|{comment.content}\n")

    def load_comments(self, thread_title: str) -> list:
        comments = []
        if os.path.exists(self.comments_file):
            with open(self.comments_file, 'r') as f:
                for line in f:
                    title, content = line.strip().split('|')
                    if title == thread_title:
                        comments.append(Comment(content))
        return comments

    def save_advice(self, advice: Advice):
        with open(self.advice_file, 'a') as f:
            f.write(f"{advice.title}|{advice.content}\n")

    def load_advice(self) -> list:
        advice_list = []
        if os.path.exists(self.advice_file):
            with open(self.advice_file, 'r') as f:
                for line in f:
                    title, content = line.strip().split('|')
                    advice_list.append(Advice(title, content))
        return advice_list

    def save_contact_inquiry(self, inquiry: ContactInquiry):
        with open(self.contact_inquiries_file, 'a') as f:
            f.write(f"{inquiry.name}|{inquiry.email}|{inquiry.message}\n")

    def load_contact_inquiries(self) -> list:
        inquiries = []
        if os.path.exists(self.contact_inquiries_file):
            with open(self.contact_inquiries_file, 'r') as f:
                for line in f:
                    name, email, message = line.strip().split('|')
                    inquiries.append(ContactInquiry(name, email, message))
        return inquiries