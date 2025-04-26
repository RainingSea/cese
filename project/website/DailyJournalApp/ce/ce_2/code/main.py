from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import urllib.parse
from datetime import datetime

class UserManager:
    def __init__(self, users_file: str):
        self.users_file = users_file
        self.load_users()

    def load_users(self):
        self.users = {}
        if os.path.exists(self.users_file):
            with open(self.users_file, 'r') as file:
                for line in file:
                    username, password = line.strip().split('|')
                    self.users[username] = password

    def register(self, username: str, password: str) -> bool:
        if username in self.users:
            return False
        self.users[username] = password
        with open(self.users_file, 'a') as file:
            file.write(f"{username}|{password}\n")
        return True

    def login(self, username: str, password: str) -> bool:
        return self.users.get(username) == password

class EntryManager:
    def __init__(self, entries_file: str):
        self.entries_file = entries_file
        self.load_entries()

    def load_entries(self):
        self.entries = []
        if os.path.exists(self.entries_file):
            with open(self.entries_file, 'r') as file:
                for line in file:
                    title, content, timestamp = line.strip().split('|')
                    self.entries.append({'title': title, 'content': content, 'timestamp': timestamp})

    def create_entry(self, title: str, content: str) -> None:
        timestamp = datetime.now().isoformat()
        self.entries.append({'title': title, 'content': content, 'timestamp': timestamp})
        with open(self.entries_file, 'a') as file:
            file.write(f"{title}|{content}|{timestamp}\n")

    def get_entries(self) -> list:
        return self.entries

class Main:
    def __init__(self):
        self.user_manager = UserManager('users.txt')
        self.entry_manager = EntryManager('entries.txt')

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
            self.wfile.write(open('templates/login.html', 'rb').read())
        elif self.path == '/register':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(open('templates/register.html', 'rb').read())
        elif self.path == '/dashboard':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(open('templates/dashboard.html', 'rb').read())
        elif self.path == '/new_entry':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(open('templates/new_entry.html', 'rb').read())
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == '/login':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            params = urllib.parse.parse_qs(post_data.decode('utf-8'))
            username = params['username'][0]
            password = params['password'][0]
            if main.user_manager.login(username, password):
                self.send_response(302)
                self.send_header('Location', '/dashboard')
                self.end_headers()
            else:
                self.send_response(401)
                self.end_headers()
        elif self.path == '/register':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            params = urllib.parse.parse_qs(post_data.decode('utf-8'))
            username = params['username'][0]
            password = params['password'][0]
            if main.user_manager.register(username, password):
                self.send_response(302)
                self.send_header('Location', '/')
                self.end_headers()
            else:
                self.send_response(400)
                self.end_headers()
        elif self.path == '/create_entry':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            params = urllib.parse.parse_qs(post_data.decode('utf-8'))
            title = params['title'][0]
            content = params['content'][0]
            main.entry_manager.create_entry(title, content)
            self.send_response(302)
            self.send_header('Location', '/dashboard')
            self.end_headers()

if __name__ == '__main__':
    main = Main()
    main.main()