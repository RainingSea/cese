import http.server
import os
import json

class UserManager:
    def __init__(self):
        self.users = self.load_users()

    def load_users(self):
        users = {}
        if os.path.exists('users.txt'):
            with open('users.txt', 'r') as file:
                for line in file:
                    username, password = line.strip().split('|')
                    users[username] = password
        return users

    def login(self, username: str, password: str) -> bool:
        return self.users.get(username) == password

    def register(self, username: str, password: str) -> bool:
        if username in self.users:
            return False
        self.users[username] = password
        with open('users.txt', 'a') as file:
            file.write(f"{username}|{password}\n")
        return True

    def get_contribution_history(self, username: str) -> list:
        contributions = []
        if os.path.exists('contributions.txt'):
            with open('contributions.txt', 'r') as file:
                for line in file:
                    user, charity_id, amount = line.strip().split('|')
                    if user == username:
                        contributions.append({'charity_id': charity_id, 'amount': float(amount)})
        return contributions

class CharityManager:
    def __init__(self):
        self.charities = self.load_charities()

    def load_charities(self):
        charities = {}
        if os.path.exists('charities.txt'):
            with open('charities.txt', 'r') as file:
                for line in file:
                    charity_id, name, description = line.strip().split('|')
                    charities[charity_id] = {'name': name, 'description': description}
        return charities

    def get_charities(self) -> list:
        return self.charities

    def get_charity_details(self, charity_id: str) -> dict:
        return self.charities.get(charity_id, {})

    def record_donation(self, username: str, charity_id: str, amount: float) -> bool:
        with open('contributions.txt', 'a') as file:
            file.write(f"{username}|{charity_id}|{amount}\n")
        return True

class Main:
    def __init__(self):
        self.user_manager = UserManager()
        self.charity_manager = CharityManager()

    def main(self):
        # Start the web server
        server_address = ('', 8000)
        httpd = http.server.HTTPServer(server_address, self.RequestHandler)
        httpd.serve_forever()

    class RequestHandler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            if self.path == '/':
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                with open('templates/login.html', 'r') as file:
                    self.wfile.write(file.read().encode())
            # Additional routes would be handled here

if __name__ == '__main__':
    app = Main()
    app.main()