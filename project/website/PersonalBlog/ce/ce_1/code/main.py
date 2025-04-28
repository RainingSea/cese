import os
import json

class User:
    def __init__(self, username: str, password: str, email: str):
        self._username = username
        self._password = password
        self._email = email

    def register(self):
        with open('users.txt', 'a') as f:
            f.write(f"{self._username}|{self._password}|{self._email}\n")

    def login(self) -> bool:
        with open('users.txt', 'r') as f:
            users = f.readlines()
            for user in users:
                u, p, _ = user.strip().split('|')
                if u == self._username and p == self._password:
                    return True
        return False

class BlogPost:
    def __init__(self, title: str, content: str, author: str):
        self._title = title
        self._content = content
        self._author = author

    def create_post(self):
        with open('posts.txt', 'a') as f:
            f.write(f"{self._title}|{self._content}|{self._author}\n")

    def edit_post(self, new_title: str, new_content: str):
        posts = []
        with open('posts.txt', 'r') as f:
            posts = f.readlines()

        with open('posts.txt', 'w') as f:
            for post in posts:
                title, content, author = post.strip().split('|')
                if title == self._title:
                    f.write(f"{new_title}|{new_content}|{author}\n")
                else:
                    f.write(post)

    def delete_post(self):
        posts = []
        with open('posts.txt', 'r') as f:
            posts = f.readlines()

        with open('posts.txt', 'w') as f:
            for post in posts:
                title, content, author = post.strip().split('|')
                if title != self._title:
                    f.write(post)

    def view_post(self) -> str:
        return f"Title: {self._title}\nContent: {self._content}\nAuthor: {self._author}"

class Main:
    def __init__(self):
        self.user = None
        self.post = None

    def main(self):
        # Placeholder for the main application logic
        pass