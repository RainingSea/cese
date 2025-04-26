import http.server
import os
import json
from urllib.parse import parse_qs, urlparse

class User:
    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email

class UserManager:
    def __init__(self):
        self.users = self.load_users()

    def load_users(self):
        users = []
        if os.path.exists('users.txt'):
            with open('users.txt', 'r') as f:
                for line in f:
                    username, password, email = line.strip().split('|')
                    users.append(User(username, password, email))
        return users

    def register(self, username, password, email):
        for user in self.users:
            if user.username == username:
                return False
        new_user = User(username, password, email)
        self.users.append(new_user)
        with open('users.txt', 'a') as f:
            f.write(f"{username}|{password}|{email}\n")
        return True

    def login(self, username, password):
        for user in self.users:
            if user.username == username and user.password == password:
                return True
        return False

class TutoringRequest:
    def __init__(self, subject, details, preferred_date):
        self.subject = subject
        self.details = details
        self.preferred_date = preferred_date

    def create_request(self):
        with open('requests.txt', 'a') as f:
            f.write(f"{self.subject}|{self.details}|{self.preferred_date}\n")
        return True

    def cancel_request(self):
        requests = []
        if os.path.exists('requests.txt'):
            with open('requests.txt', 'r') as f:
                requests = [line.strip().split('|') for line in f]
        
        if requests:
            requests.pop()  # Remove the last request
            with open('requests.txt', 'w') as f:
                for req in requests:
                    f.write('|'.join(req) + '\n')
            return True
        return False

class Contact:
    def __init__(self, name, email, message):
        self.name = name
        self.email = email
        self.message = message

    def send_message(self):
        with open('contacts.txt', 'a') as f:
            f.write(f"{self.name}|{self.email}|{self.message}\n")
        return True

class Main(http.server.SimpleHTTPRequestHandler):
    user_manager = UserManager()
    logged_in_user = None

    def do_GET(self):
        parsed_path = urlparse(self.path)
        if parsed_path.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(self.render_login_page().encode())
        elif parsed_path.path == '/register':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(self.render_register_page().encode())
        elif parsed_path.path == '/dashboard':
            if self.logged_in_user:
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(self.render_dashboard_page().encode())
            else:
                self.send_response(302)
                self.send_header('Location', '/')
                self.end_headers()
        elif parsed_path.path == '/contact':
            if self.logged_in_user:
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(self.render_contact_page().encode())
            else:
                self.send_response(302)
                self.send_header('Location', '/')
                self.end_headers()
        elif parsed_path.path == '/logout':
            self.logged_in_user = None
            self.send_response(302)
            self.send_header('Location', '/')
            self.end_headers()
        elif parsed_path.path == '/cancel_request':
            if self.logged_in_user:
                tutoring_request = TutoringRequest("", "", "")
                if tutoring_request.cancel_request():
                    self.send_response(302)
                    self.send_header('Location', '/dashboard')
                    self.end_headers()
                else:
                    self.send_response(400)
                    self.end_headers()
            else:
                self.send_response(302)
                self.send_header('Location', '/')
                self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        parsed_path = urlparse(self.path)
        if parsed_path.path == '/login':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = parse_qs(post_data.decode())
            username = data['username'][0]
            password = data['password'][0]
            if self.user_manager.login(username, password):
                self.logged_in_user = username
                self.send_response(302)
                self.send_header('Location', '/dashboard')
                self.end_headers()
            else:
                self.send_response(401)
                self.end_headers()
        elif parsed_path.path == '/register':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = parse_qs(post_data.decode())
            username = data['username'][0]
            password = data['password'][0]
            email = data['email'][0]
            if self.user_manager.register(username, password, email):
                self.send_response(302)
                self.send_header('Location', '/')
                self.end_headers()
            else:
                self.send_response(400)
                self.end_headers()
        elif parsed_path.path == '/contact':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = parse_qs(post_data.decode())
            name = data['name'][0]
            email = data['email'][0]
            message = data['message'][0]
            contact = Contact(name, email, message)
            contact.send_message()
            self.send_response(302)
            self.send_header('Location', '/dashboard')
            self.end_headers()

    def render_login_page(self):
        with open('templates/login.html', 'r') as f:
            return f.read()

    def render_register_page(self):
        with open('templates/register.html', 'r') as f:
            return f.read()

    def render_dashboard_page(self):
        with open('templates/dashboard.html', 'r') as f:
            return f.read()

    def render_contact_page(self):
        with open('templates/contact.html', 'r') as f:
            return f.read()

if __name__ == "__main__":
    server_address = ('', 8000)
    httpd = http.server.HTTPServer(server_address, Main)
    print("Server started at http://localhost:8000")
    httpd.serve_forever()