import http.server
import socketserver
import os
import json

class Main:
    def __init__(self, port=8000):
        self.port = port
        self.server = http.server.HTTPServer(("", self.port), self.RequestHandler)
        self.load_data()

    def load_data(self):
        self.users = self.load_users()
        self.feedbacks = self.load_feedbacks()
        self.statuses = self.load_statuses()

    def load_users(self):
        if os.path.exists('users.txt'):
            with open('users.txt', 'r') as file:
                return [line.strip().split('|') for line in file.readlines()]
        return []

    def load_feedbacks(self):
        if os.path.exists('feedback.txt'):
            with open('feedback.txt', 'r') as file:
                return [json.loads(line.strip()) for line in file.readlines()]
        return []

    def load_statuses(self):
        if os.path.exists('status.txt'):
            with open('status.txt', 'r') as file:
                return json.load(file)
        return {}

    def main(self):
        print(f"Starting server on port {self.port}...")
        self.server.serve_forever()

    class RequestHandler(http.server.SimpleHTTPRequestHandler):
        def do_GET(self):
            if self.path == '/':
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(open('templates/login.html', 'rb').read())
            elif self.path == '/register':
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(open('templates/register.html', 'rb').read())
            elif self.path == '/feedback':
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(open('templates/feedback.html', 'rb').read())
            else:
                self.send_error(404)

if __name__ == "__main__":
    app = Main()
    app.main()