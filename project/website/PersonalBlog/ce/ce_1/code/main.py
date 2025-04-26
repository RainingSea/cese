from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import urllib.parse

class Main:
    def __init__(self):
        self.user_manager = UserManager('users.txt')
        self.post_manager = PostManager('posts.txt')

    def main(self):
        server_address = ('', 8080)
        httpd = HTTPServer(server_address, RequestHandler)
        httpd.serve_forever()

class UserManager:
    def __init__(self, filename: str):
        self.filename = filename
        self.users = self.load_users()

    def register(self, username: str, password: str, email: str) -> bool:
        if username in self.users:
            return False
        with open(self.filename, 'a') as file:
            file.write(f"{username}|{password}|{email}\n")
        self.users[username] = (password, email)
        return True

    def login(self, username: str, password: str) -> bool:
        return username in self.users and self.users[username][0] == password

    def load_users(self) -> dict:
        users = {}
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as file:
                for line in file:
                    username, password, email = line.strip().split('|')
                    users[username] = (password, email)
        return users

class PostManager:
    def __init__(self, filename: str):
        self.filename = filename
        self.posts = self.load_posts()

    def create_post(self, title: str, content: str, username: str) -> bool:
        if title in self.posts:
            return False
        with open(self.filename, 'a') as file:
            file.write(f"{title}|{content}|{username}\n")
        self.posts[title] = (content, username)
        return True

    def edit_post(self, title: str, new_content: str) -> bool:
        if title not in self.posts:
            return False
        self.posts[title] = (new_content, self.posts[title][1])
        self.save_posts()
        return True

    def delete_post(self, title: str) -> bool:
        if title not in self.posts:
            return False
        del self.posts[title]
        self.save_posts()
        return True

    def load_posts(self) -> dict:
        posts = {}
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as file:
                for line in file:
                    title, content, username = line.strip().split('|')
                    posts[title] = (content, username)
        return posts

    def save_posts(self):
        with open(self.filename, 'w') as file:
            for title, (content, username) in self.posts.items():
                file.write(f"{title}|{content}|{username}\n")

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        if parsed_path.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(bytes(self.load_template('templates/login.html'), 'utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

    def load_template(self, filename):
        with open(filename, 'r') as file:
            return file.read()

if __name__ == '__main__':
    app = Main()
    app.main()