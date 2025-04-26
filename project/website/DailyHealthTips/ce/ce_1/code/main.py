from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import urllib.parse

class DailyHealthTipsApp:
    def __init__(self):
        self.user_manager = UserManager()
        self.tip_manager = TipManager()
        self.feedback_manager = FeedbackManager()

    def run(self):
        server_address = ('', 8000)
        httpd = HTTPServer(server_address, self)
        print("Starting server on port 8000...")
        httpd.serve_forever()

    def __call__(self, *args):
        return RequestHandler(self, *args)

class RequestHandler(BaseHTTPRequestHandler):
    def __init__(self, app, *args):
        self.app = app
        super().__init__(*args)

    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        if parsed_path.path == '/':
            self.handle_login()
        elif parsed_path.path == '/tips':
            self.handle_tips()
        elif parsed_path.path == '/archive':
            self.handle_archive()
        elif parsed_path.path == '/feedback':
            self.handle_feedback()
        else:
            self.send_error(404)

    def do_POST(self):
        parsed_path = urllib.parse.urlparse(self.path)
        if parsed_path.path == '/login':
            self.handle_login_post()
        elif parsed_path.path == '/register':
            self.handle_register_post()
        elif parsed_path.path == '/submit_feedback':
            self.handle_feedback_post()
        else:
            self.send_error(404)

    def handle_login(self):
        with open('templates/login.html', 'r') as f:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(f.read().encode())

    def handle_tips(self):
        current_tip = self.app.tip_manager.get_current_tip()
        with open('templates/tips.html', 'r') as f:
            content = f.read().replace('{{ current_tip }}', current_tip)
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(content.encode())

    def handle_archive(self):
        tips = self.app.tip_manager.tips
        with open('templates/archive.html', 'r') as f:
            content = f.read().replace('{{ tips }}', '<br>'.join(tips))
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(content.encode())

    def handle_feedback(self):
        with open('templates/feedback.html', 'r') as f:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(f.read().encode())

    def handle_login_post(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode()
        username, password = urllib.parse.parse_qs(post_data)['username'][0], urllib.parse.parse_qs(post_data)['password'][0]
        if self.app.user_manager.login(username, password):
            self.send_response(302)
            self.send_header('Location', '/tips')
            self.end_headers()
        else:
            self.send_error(401)

    def handle_register_post(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode()
        username, password = urllib.parse.parse_qs(post_data)['username'][0], urllib.parse.parse_qs(post_data)['password'][0]
        if self.app.user_manager.register(username, password):
            self.send_response(302)
            self.send_header('Location', '/')
            self.end_headers()
        else:
            self.send_error(400)

    def handle_feedback_post(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode()
        feedback = urllib.parse.parse_qs(post_data)['feedback'][0]
        self.app.feedback_manager.submit_feedback(feedback)
        self.send_response(302)
        self.send_header('Location', '/feedback')
        self.end_headers()

class UserManager:
    def __init__(self):
        self.users = self.load_users()

    def load_users(self):
        if not os.path.exists('users.txt'):
            return []
        with open('users.txt', 'r') as f:
            return [line.strip().split('|') for line in f.readlines()]

    def login(self, username: str, password: str) -> bool:
        for user in self.users:
            if user[0] == username and user[1] == password:
                return True
        return False

    def register(self, username: str, password: str) -> bool:
        if any(user[0] == username for user in self.users):
            return False
        self.users.append([username, password])
        with open('users.txt', 'a') as f:
            f.write(f"{username}|{password}\n")
        return True

class TipManager:
    def __init__(self):
        self.tips = self.load_tips()

    def load_tips(self):
        if not os.path.exists('tips.txt'):
            return []
        with open('tips.txt', 'r') as f:
            return [line.strip() for line in f.readlines()]

    def get_current_tip(self) -> str:
        return self.tips[0] if self.tips else "No tips available."

class FeedbackManager:
    def __init__(self):
        self.feedbacks = self.load_feedbacks()

    def load_feedbacks(self):
        if not os.path.exists('feedback.txt'):
            return []
        with open('feedback.txt', 'r') as f:
            return [line.strip() for line in f.readlines()]

    def submit_feedback(self, feedback: str) -> None:
        self.feedbacks.append(feedback)
        with open('feedback.txt', 'a') as f:
            f.write(f"{feedback}\n")

if __name__ == "__main__":
    app = DailyHealthTipsApp()
    app.run(port=8152, debug=False)
