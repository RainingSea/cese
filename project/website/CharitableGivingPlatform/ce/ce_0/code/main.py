from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import json

class Main:
    def __init__(self):
        self.user_manager = UserManager('users.txt')
        self.charity_manager = CharityManager('charities.txt')

    def main(self):
        server_address = ('', 8080)
        httpd = HTTPServer(server_address, RequestHandler)
        print("Server running on port 8080...")
        httpd.serve_forever()

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
            with open('templates/register.html', 'r') as file:
                self.wfile.write(file.read().encode())
        elif self.path == '/dashboard':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('templates/dashboard.html', 'r') as file:
                self.wfile.write(file.read().encode())
        elif self.path.startswith('/charity_details'):
            charity_name = self.path.split('=')[1]
            details = self.server.charity_manager.get_charity_details(charity_name)
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(details.encode())

    def do_POST(self):
        # Handle POST requests for login, registration, and donations
        pass

class UserManager:
    def __init__(self, users_file: str):
        self.users_file = users_file
        self.load_users()

    def load_users(self):
        self.users = {}
        if os.path.exists(self.users_file):
            with open(self.users_file, 'r') as file:
                for line in file:
                    username, password = line.strip().split(',')
                    self.users[username] = password

    def login(self, username: str, password: str) -> bool:
        return self.users.get(username) == password

    def register(self, username: str, password: str) -> bool:
        if username in self.users:
            return False
        self.users[username] = password
        with open(self.users_file, 'a') as file:
            file.write(f"{username},{password}\n")
        return True

    def get_user_contributions(self, username: str) -> list:
        return []

class CharityManager:
    def __init__(self, charities_file: str):
        self.charities_file = charities_file
        self.load_charities()

    def load_charities(self):
        self.charities = {}
        if os.path.exists(self.charities_file):
            with open(self.charities_file, 'r') as file:
                for line in file:
                    name, mission, ongoing_projects = line.strip().split(',')
                    self.charities[name] = {
                        'mission': mission,
                        'ongoing_projects': ongoing_projects.split(';')
                    }

    def get_charities(self) -> list:
        return list(self.charities.keys())

    def get_charity_details(self, name: str) -> str:
        charity = self.charities.get(name)
        if charity:
            details = f"Mission: {charity['mission']}<br>Ongoing Projects: {', '.join(charity['ongoing_projects'])}"
            return details
        return "Charity not found."

    def record_donation(self, username: str, charity_name: str, amount: float) -> None:
        with open('donations.txt', 'a') as file:
            file.write(f"{username},{charity_name},{amount},{self.get_current_date()}\n")

    def get_current_date(self):
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d")

if __name__ == '__main__':
    app = Main()
    app.main()