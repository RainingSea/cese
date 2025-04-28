from http.server import BaseHTTPRequestHandler, HTTPServer
import os
from UserManager import UserManager
from TaskManager import TaskManager

class Main:
    def __init__(self):
        self.user_manager = UserManager('users.txt')
        self.task_manager = TaskManager('tasks_template.txt')

    def run(self):
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
            with open('templates/login.html', 'r') as f:
                self.wfile.write(f.read().encode())
        elif self.path == '/register':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('templates/register.html', 'r') as f:
                self.wfile.write(f.read().encode())
        elif self.path == '/home':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('templates/home.html', 'r') as f:
                self.wfile.write(f.read().encode())
        else:
            self.send_response(404)
            self.end_headers()

if __name__ == '__main__':
    main_app = Main()
    main_app.run()