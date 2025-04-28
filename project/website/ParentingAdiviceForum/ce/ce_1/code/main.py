import os
import json

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

class Thread:
    def __init__(self, thread_id, title, content):
        self.thread_id = thread_id
        self.title = title
        self.content = content

class Comment:
    def __init__(self, comment_id, thread_id, content):
        self.comment_id = comment_id
        self.thread_id = thread_id
        self.content = content

class Contact:
    def __init__(self, name, email, message):
        self.name = name
        self.email = email
        self.message = message

class UserManager:
    def __init__(self):
        self.users = self.load_users()

    def load_users(self):
        if not os.path.exists('users.txt'):
            return []
        with open('users.txt', 'r') as file:
            return [User(*line.strip().split('|')) for line in file.readlines()]

    def register(self, username: str, password: str) -> bool:
        if any(user.username == username for user in self.users):
            return False
        self.users.append(User(username, password))
        self.save_users()
        return True

    def save_users(self):
        with open('users.txt', 'w') as file:
            for user in self.users:
                file.write(f"{user.username}|{user.password}\n")

    def login(self, username: str, password: str) -> bool:
        return any(user.username == username and user.password == password for user in self.users)

    def updateProfile(self, username: str, new_info: dict) -> bool:
        for user in self.users:
            if user.username == username:
                user.password = new_info.get('password', user.password)
                self.save_users()
                return True
        return False

    def deleteAccount(self, username: str) -> bool:
        self.users = [user for user in self.users if user.username != username]
        self.save_users()
        return True

class ThreadManager:
    def __init__(self):
        self.threads = self.load_threads()

    def load_threads(self):
        if not os.path.exists('threads.txt'):
            return []
        with open('threads.txt', 'r') as file:
            return [Thread(*line.strip().split('|')) for line in file.readlines()]

    def createThread(self, title: str, content: str) -> bool:
        thread_id = len(self.threads) + 1
        self.threads.append(Thread(thread_id, title, content))
        self.save_threads()
        return True

    def save_threads(self):
        with open('threads.txt', 'w') as file:
            for thread in self.threads:
                file.write(f"{thread.thread_id}|{thread.title}|{thread.content}\n")

    def getThreads(self):
        return self.threads

    def getThreadDetails(self, thread_id: int) -> Thread:
        for thread in self.threads:
            if thread.thread_id == thread_id:
                return thread
        return None

class CommentManager:
    def __init__(self):
        self.comments = self.load_comments()

    def load_comments(self):
        if not os.path.exists('comments.txt'):
            return []
        with open('comments.txt', 'r') as file:
            return [Comment(*line.strip().split('|')) for line in file.readlines()]

    def addComment(self, thread_id: int, content: str) -> bool:
        comment_id = len(self.comments) + 1
        self.comments.append(Comment(comment_id, thread_id, content))
        self.save_comments()
        return True

    def save_comments(self):
        with open('comments.txt', 'w') as file:
            for comment in self.comments:
                file.write(f"{comment.comment_id}|{comment.thread_id}|{comment.content}\n")

    def getComments(self, thread_id: int):
        return [comment for comment in self.comments if comment.thread_id == thread_id]

class ContactManager:
    def __init__(self):
        self.contacts = self.load_contacts()

    def load_contacts(self):
        if not os.path.exists('contacts.txt'):
            return []
        with open('contacts.txt', 'r') as file:
            return [Contact(*line.strip().split('|')) for line in file.readlines()]

    def submitInquiry(self, name: str, email: str, message: str) -> bool:
        self.contacts.append(Contact(name, email, message))
        self.save_contacts()
        return True

    def save_contacts(self):
        with open('contacts.txt', 'w') as file:
            for contact in self.contacts:
                file.write(f"{contact.name}|{contact.email}|{contact.message}\n")

class Main:
    def __init__(self):
        self.user_manager = UserManager()
        self.thread_manager = ThreadManager()
        self.comment_manager = CommentManager()
        self.contact_manager = ContactManager()

    def main(self):
        # Placeholder for routing logic (Flask or another framework would be used here)
        pass

if __name__ == "__main__":
    app = Main()
    app.main()