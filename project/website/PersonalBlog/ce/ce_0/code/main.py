import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
from user_manager import UserManager
from post_manager import PostManager

class Main:
    def __init__(self):
        self.user_manager = UserManager('users.txt')
        self.post_manager = PostManager('posts.txt')

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
            with open('templates/login.html', 'r') as f:
                self.wfile.write(f.read().encode())
        # Additional routes will be handled here...

    def do_POST(self):
        # Handle POST requests for login and registration
        pass

if __name__ == "__main__":
    app = Main()
    app.main()