from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import json

class Main:
    def __init__(self):
        self.user_manager = UserManager()
        self.medical_info_manager = MedicalInfoManager()
        self.reminder_manager = ReminderManager()

    def main(self):
        server_address = ('', 8080)
        httpd = HTTPServer(server_address, RequestHandler)
        print("Starting server on port 8080...")
        httpd.serve_forever()

class UserManager:
    def __init__(self):
        self.users = self.load_users()

    def load_users(self):
        if not os.path.exists('users.txt'):
            return {}
        with open('users.txt', 'r') as file:
            return {line.split('|')[0]: line.split('|')[1].strip() for line in file.readlines()}

    def register(self, username: str, password: str) -> bool:
        if username in self.users:
            return False
        self.users[username] = password
        with open('users.txt', 'a') as file:
            file.write(f"{username}|{password}\n")
        return True

    def login(self, username: str, password: str) -> bool:
        return self.users.get(username) == password

class MedicalInfoManager:
    def __init__(self):
        self.medical_info = self.load_medical_info()

    def load_medical_info(self):
        if not os.path.exists('medical_info.txt'):
            return {}
        with open('medical_info.txt', 'r') as file:
            return {line.split('|')[0]: line.split('|')[1].strip() for line in file.readlines()}

    def add_medical_info(self, user: str, info: str) -> bool:
        self.medical_info[user] = info
        with open('medical_info.txt', 'a') as file:
            file.write(f"{user}|{info}\n")
        return True

    def get_medical_info(self, user: str) -> str:
        return self.medical_info.get(user, "")

class ReminderManager:
    def __init__(self):
        self.reminders = self.load_reminders()

    def load_reminders(self):
        if not os.path.exists('reminders.txt'):
            return {}
        with open('reminders.txt', 'r') as file:
            return {line.split('|')[0]: line.split('|')[1].strip() for line in file.readlines()}

    def set_reminder(self, user: str, reminder: str) -> bool:
        self.reminders[user] = reminder
        with open('reminders.txt', 'a') as file:
            file.write(f"{user}|{reminder}\n")
        return True

    def get_reminders(self, user: str) -> str:
        return self.reminders.get(user, "")

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('templates/login.html', 'r') as file:
                self.wfile.write(file.read().encode())
        elif self.path == '/register':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('templates/registration.html', 'r') as file:
                self.wfile.write(file.read().encode())
        elif self.path == '/dashboard':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('templates/dashboard.html', 'r') as file:
                self.wfile.write(file.read().encode())
        else:
            self.send_response(404)
            self.end_headers()

if __name__ == "__main__":
    app = Main()
    app.main()