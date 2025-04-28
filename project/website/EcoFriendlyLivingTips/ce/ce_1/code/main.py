import http.server
import os
import json

class Main:
    def __init__(self):
        self.user_manager = UserManager()
        self.tip_manager = TipManager()
        self.resource_manager = ResourceManager()
        self.forum_manager = ForumManager()

    def main(self):
        server_address = ('', 8000)
        httpd = http.server.HTTPServer(server_address, RequestHandler)
        print("Starting server on port 8000...")
        httpd.serve_forever()

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

    def create_account(self, username: str, password: str) -> bool:
        if username in self.users:
            return False
        self.users[username] = password
        with open('users.txt', 'a') as file:
            file.write(f"{username}|{password}\n")
        return True

class TipManager:
    def __init__(self):
        self.tips = self.load_tips()

    def load_tips(self):
        tips = []
        if os.path.exists('tips.txt'):
            with open('tips.txt', 'r') as file:
                tips = [line.strip() for line in file]
        return tips

    def view_tips(self) -> list:
        return self.tips

    def submit_tip(self, tip: str) -> bool:
        self.tips.append(tip)
        with open('tips.txt', 'a') as file:
            file.write(f"{tip}\n")
        return True

class ResourceManager:
    def __init__(self):
        self.resources = self.load_resources()

    def load_resources(self):
        resources = []
        if os.path.exists('resources.txt'):
            with open('resources.txt', 'r') as file:
                resources = [line.strip() for line in file]
        return resources

    def view_resources(self) -> list:
        return self.resources

    def add_resource(self, resource: str) -> bool:
        self.resources.append(resource)
        with open('resources.txt', 'a') as file:
            file.write(f"{resource}\n")
        return True

class ForumManager:
    def __init__(self):
        self.posts = self.load_posts()

    def load_posts(self):
        posts = []
        if os.path.exists('forum.txt'):
            with open('forum.txt', 'r') as file:
                posts = [line.strip() for line in file]
        return posts

    def view_posts(self) -> list:
        return self.posts

    def add_post(self, post: str) -> bool:
        self.posts.append(post)
        with open('forum.txt', 'a') as file:
            file.write(f"{post}\n")
        return True

class RequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('templates/login.html', 'r') as file:
                self.wfile.write(file.read().encode())
        # Additional routing for other pages would go here

if __name__ == '__main__':
    app = Main()
    app.main()