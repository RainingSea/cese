from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import urllib.parse
from urllib.parse import parse_qs
from user_manager import UserManager
from destination_recommender import DestinationRecommender

class Main:
    def __init__(self):
        self.user_manager = UserManager()
        self.recommender = DestinationRecommender()
        self.recommender.load_destinations()
        self.user_manager.load_user_data()

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
            with open('templates/login.html', 'r') as file:
                self.wfile.write(file.read().encode())
        elif self.path == '/register':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('templates/registration.html', 'r') as file:
                self.wfile.write(file.read().encode())
        elif self.path == '/preferences':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('templates/preferences.html', 'r') as file:
                self.wfile.write(file.read().encode())
        elif self.path == '/recommendations':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('templates/recommendations.html', 'r') as file:
                self.wfile.write(file.read().encode())
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == '/register':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = parse_qs(post_data.decode())
            username = data['username'][0]
            password = data['password'][0]
            if self.server.user_manager.register(username, password):
                self.send_response(302)
                self.send_header('Location', '/')
                self.end_headers()
            else:
                self.send_response(400)
                self.end_headers()
        elif self.path == '/login':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = parse_qs(post_data.decode())
            username = data['username'][0]
            password = data['password'][0]
            if self.server.user_manager.login(username, password):
                self.send_response(302)
                self.send_header('Location', '/preferences')
                self.end_headers()
            else:
                self.send_response(401)
                self.end_headers()

if __name__ == '__main__':
    app = Main()
    app.main()