import os
import json

class Main:
    def __init__(self):
        self.users = self.load_users()
        self.threads = self.load_threads()
        self.comments = self.load_comments()
        self.contacts = self.load_contacts()

    def main(self):
        # Placeholder for main application logic
        print("Welcome to Parenting Advice Forum!")

    def load_users(self):
        users = []
        if os.path.exists('users.txt'):
            with open('users.txt', 'r') as file:
                for line in file:
                    username, password = line.strip().split('|')
                    users.append(User(username, password))
        return users

    def load_threads(self):
        threads = []
        if os.path.exists('threads.txt'):
            with open('threads.txt', 'r') as file:
                for line in file:
                    title, content = line.strip().split('|')
                    threads.append(Thread(title, content))
        return threads

    def load_comments(self):
        comments = []
        if os.path.exists('comments.txt'):
            with open('comments.txt', 'r') as file:
                for line in file:
                    thread_id, content, author = line.strip().split('|')
                    comments.append(Comment(content, author))
        return comments

    def load_contacts(self):
        contacts = []
        if os.path.exists('contacts.txt'):
            with open('contacts.txt', 'r') as file:
                for line in file:
                    name, email, message = line.strip().split('|')
                    contacts.append(Contact(name, email, message))
        return contacts

    def login(self, username: str, password: str) -> bool:
        for user in self.users:
            if user.username == username and user.password == password:
                return True
        return False

    def register(self, username: str, password: str) -> bool:
        if any(user.username == username for user in self.users):
            return False
        self.users.append(User(username, password))
        with open('users.txt', 'a') as file:
            file.write(f"{username}|{password}\n")
        return True

    def create_thread(self, title: str, content: str) -> bool:
        new_thread = Thread(title, content)
        self.threads.append(new_thread)
        with open('threads.txt', 'a') as file:
            file.write(f"{title}|{content}\n")
        return True

    def post_comment(self, thread_id: int, comment: str) -> bool:
        if 0 <= thread_id < len(self.threads):
            self.threads[thread_id].add_comment(comment)
            with open('comments.txt', 'a') as file:
                file.write(f"{thread_id}|{comment}|{self.get_current_user()}\n")
            return True
        return False

    def post_advice(self, title: str, content: str) -> bool:
        return self.create_thread(title, content)

    def update_profile(self, username: str, new_info: dict) -> bool:
        for user in self.users:
            if user.username == username:
                user.username = new_info.get('username', user.username)
                user.password = new_info.get('password', user.password)
                self.save_users()
                return True
        return False

    def contact_admin(self, name: str, email: str, message: str) -> bool:
        new_contact = Contact(name, email, message)
        self.contacts.append(new_contact)
        with open('contacts.txt', 'a') as file:
            file.write(f"{name}|{email}|{message}\n")
        return True

    def get_current_user(self):
        # Placeholder for getting the currently logged-in user
        return "current_user"

class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def get_profile(self) -> dict:
        return {"username": self.username}

    def delete_account(self) -> bool:
        # Placeholder for account deletion logic
        return True

class Thread:
    def __init__(self, title: str, content: str):
        self.title = title
        self.content = content
        self.comments = []

    def add_comment(self, comment: str) -> bool:
        self.comments.append(Comment(comment, "author_placeholder"))  # Placeholder for author
        return True

class Comment:
    def __init__(self, content: str, author: str):
        self.content = content
        self.author = author

class Contact:
    def __init__(self, name: str, email: str, message: str):
        self.name = name
        self.email = email
        self.message = message

    def send(self) -> bool:
        # Placeholder for sending contact message logic
        return True

if __name__ == "__main__":
    app = Main()
    app.main()