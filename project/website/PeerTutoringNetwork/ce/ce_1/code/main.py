import http.server
import os
import json

class Main:
    def __init__(self):
        self.user_manager = UserManager()
        self.tutoring_request_manager = TutoringRequestManager()
        self.support_manager = SupportManager()

    def main(self):
        server_address = ('', 8080)
        httpd = http.server.HTTPServer(server_address, self)
        print("Starting server on port 8080...")
        httpd.serve_forever()

    def do_GET(self):
        if self.path == '/':
            self.handle_login()
        elif self.path == '/register':
            self.handle_registration()
        elif self.path == '/dashboard':
            self.handle_dashboard()
        elif self.path == '/view_tutors':
            self.handle_view_tutors()
        elif self.path == '/request_tutoring':
            self.handle_request_tutoring()
        elif self.path == '/profile':
            self.handle_profile()
        elif self.path == '/contact':
            self.handle_contact()
        else:
            self.send_response(404)
            self.end_headers()

    def handle_login(self):
        with open('templates/login.html', 'r') as file:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(file.read().encode())

    def handle_registration(self):
        with open('templates/registration.html', 'r') as file:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(file.read().encode())

    def handle_dashboard(self):
        with open('templates/dashboard.html', 'r') as file:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(file.read().encode())

    def handle_view_tutors(self):
        with open('templates/view_tutors.html', 'r') as file:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(file.read().encode())

    def handle_request_tutoring(self):
        with open('templates/request_tutoring.html', 'r') as file:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(file.read().encode())

    def handle_profile(self):
        with open('templates/profile.html', 'r') as file:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(file.read().encode())

    def handle_contact(self):
        with open('templates/contact.html', 'r') as file:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(file.read().encode())

class UserManager:
    def __init__(self):
        self.users = self.load_users()

    def load_users(self):
        if not os.path.exists('users.txt'):
            return []
        with open('users.txt', 'r') as file:
            return [line.strip().split('|') for line in file.readlines()]

    def login(self, username: str, password: str) -> bool:
        for user in self.users:
            if user[0] == username and user[1] == password:
                return True
        return False

    def register(self, username: str, password: str, email: str) -> bool:
        if any(user[0] == username for user in self.users):
            return False
        with open('users.txt', 'a') as file:
            file.write(f"{username}|{password}|{email}\n")
        self.users.append([username, password, email])
        return True

    def get_user_profile(self, username: str) -> dict:
        for user in self.users:
            if user[0] == username:
                return {'username': user[0], 'email': user[2]}
        return {}

class TutoringRequestManager:
    def __init__(self):
        self.requests = self.load_requests()

    def load_requests(self):
        if not os.path.exists('tutoring_requests.txt'):
            return []
        with open('tutoring_requests.txt', 'r') as file:
            return [line.strip().split('|') for line in file.readlines()]

    def create_request(self, subject: str, details: str, date: str) -> bool:
        request_id = len(self.requests) + 1
        with open('tutoring_requests.txt', 'a') as file:
            file.write(f"{request_id}|{subject}|{details}|{date}\n")
        self.requests.append([request_id, subject, details, date])
        return True

    def cancel_request(self, request_id: int) -> bool:
        for request in self.requests:
            if int(request[0]) == request_id:
                self.requests.remove(request)
                self.save_requests()
                return True
        return False

    def save_requests(self):
        with open('tutoring_requests.txt', 'w') as file:
            for request in self.requests:
                file.write('|'.join(map(str, request)) + '\n')

    def view_requests(self) -> list:
        return self.requests

class SupportManager:
    def __init__(self):
        self.messages = self.load_messages()

    def load_messages(self):
        if not os.path.exists('support_messages.txt'):
            return []
        with open('support_messages.txt', 'r') as file:
            return [line.strip().split('|') for line in file.readlines()]

    def send_message(self, name: str, email: str, message: str) -> bool:
        with open('support_messages.txt', 'a') as file:
            file.write(f"{name}|{email}|{message}\n")
        self.messages.append([name, email, message])
        return True

if __name__ == "__main__":
    app = Main()
    app.main()