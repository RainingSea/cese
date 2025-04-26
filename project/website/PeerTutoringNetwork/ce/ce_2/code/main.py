import http.server
import os
import json

class User:
    def __init__(self, username: str, password: str, email: str):
        self.username = username
        self.password = password
        self.email = email

    def register(self, username: str, password: str, email: str) -> bool:
        with open('users.txt', 'a') as f:
            f.write(f"{username}|{password}|{email}\n")
        return True

    def login(self, username: str, password: str) -> bool:
        with open('users.txt', 'r') as f:
            for line in f:
                stored_username, stored_password, _ = line.strip().split('|')
                if stored_username == username and stored_password == password:
                    return True
        return False

class TutoringRequest:
    def __init__(self, subject: str, details: str, preferred_date: str):
        self.subject = subject
        self.details = details
        self.preferred_date = preferred_date

    def create_request(self, subject: str, details: str, preferred_date: str) -> bool:
        with open('requests.txt', 'a') as f:
            f.write(f"{subject}|{details}|{preferred_date}\n")
        return True

class Contact:
    def __init__(self, name: str, email: str, message: str):
        self.name = name
        self.email = email
        self.message = message

    def send_message(self, name: str, email: str, message: str) -> bool:
        with open('contacts.txt', 'a') as f:
            f.write(f"{name}|{email}|{message}\n")
        return True

class Main:
    @staticmethod
    def main() -> str:
        return "Welcome to the Tutoring Application"

class SimpleHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(bytes(open('templates/login.html').read(), 'utf-8'))
        else:
            super().do_GET()

if __name__ == "__main__":
    httpd = http.server.HTTPServer(('localhost', 8000), SimpleHTTPRequestHandler)
    print("Serving on port 8000...")
    httpd.serve_forever()