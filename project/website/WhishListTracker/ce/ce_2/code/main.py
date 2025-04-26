import os
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse

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

    def register(self, username: str, password: str) -> bool:
        if username in self.users:
            return False
        self.users[username] = password
        with open(self.users_file, 'a') as file:
            file.write(f"{username},{password}\n")
        return True

    def login(self, username: str, password: str) -> bool:
        return self.users.get(username) == password

class WishlistManager:
    def __init__(self, wishlist_file: str):
        self.wishlist_file = wishlist_file

    def add_item(self, username: str, item_name: str, description: str, price: float) -> bool:
        wishlist_file = f"wishlist_{username}.txt"
        with open(wishlist_file, 'a') as file:
            file.write(f"{item_name},{description},{price}\n")
        return True

    def view_wishlist(self, username: str) -> list:
        wishlist_file = f"wishlist_{username}.txt"
        items = []
        if os.path.exists(wishlist_file):
            with open(wishlist_file, 'r') as file:
                for line in file:
                    items.append(line.strip().split(','))
        return items

    def update_item(self, username: str, item_name: str, new_description: str, new_price: float) -> bool:
        wishlist_file = f"wishlist_{username}.txt"
        items = self.view_wishlist(username)
        updated = False
        with open(wishlist_file, 'w') as file:
            for item in items:
                if item[0] == item_name:
                    file.write(f"{item_name},{new_description},{new_price}\n")
                    updated = True
                else:
                    file.write(','.join(item) + '\n')
        return updated

    def remove_item(self, username: str, item_name: str) -> bool:
        wishlist_file = f"wishlist_{username}.txt"
        items = self.view_wishlist(username)
        updated = False
        with open(wishlist_file, 'w') as file:
            for item in items:
                if item[0] != item_name:
                    file.write(','.join(item) + '\n')
                else:
                    updated = True
        return updated

class Main:
    def __init__(self):
        self.user_manager = UserManager('users.txt')
        self.wishlist_manager = WishlistManager('wishlist_template.txt')

    def main(self):
        server_address = ('', 8000)
        httpd = HTTPServer(server_address, RequestHandler)
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
            with open('templates/registration.html', 'r') as file:
                self.wfile.write(file.read().encode())
        elif self.path == '/dashboard':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('templates/dashboard.html', 'r') as file:
                self.wfile.write(file.read().encode())

    def do_POST(self):
        parsed_path = urlparse(self.path)
        if parsed_path.path == '/login':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = parse_qs(post_data.decode())
            username = data['username'][0]
            password = data['password'][0]
            if self.server.main.user_manager.login(username, password):
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
            if self.server.main.user_manager.register(username, password):
                self.send_response(302)
                self.send_header('Location', '/')
                self.end_headers()
            else:
                self.send_response(409)
                self.end_headers()

if __name__ == '__main__':
    app = Main()
    app.main()