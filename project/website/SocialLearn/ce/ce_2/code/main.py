from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
import json
from user_manager import UserManager
from profile_manager import ProfileManager
from group_manager import GroupManager
from resource_manager import ResourceManager
from message_manager import MessageManager

class Main:
    def __init__(self):
        self.user_manager = UserManager()
        self.profile_manager = ProfileManager()
        self.group_manager = GroupManager()
        self.resource_manager = ResourceManager()
        self.message_manager = MessageManager()
    
    def main(self):
        server_address = ('', 8080)
        httpd = HTTPServer(server_address, RequestHandler)
        print("Starting server on port 8080...")
        httpd.serve_forever()

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('templates/login.html', 'r') as f:
                self.wfile.write(f.read().encode())
        # Additional routes would be handled here...

    def do_POST(self):
        # Handle POST requests for login, registration, etc.
        pass

if __name__ == "__main__":
    app = Main()
    app.main()