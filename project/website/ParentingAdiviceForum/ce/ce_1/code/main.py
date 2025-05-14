import http.server
import socketserver
import json
import os
from urllib.parse import parse_qs, urlparse

class FileManager:
    def read_data(self, filename):
        try:
            with open(filename, 'r') as file:
                return [line.strip() for line in file.readlines()]
        except FileNotFoundError:
            return []

    def write_data(self, filename, data):
        with open(filename, 'w') as file:
            if isinstance(data, list):
                file.write('\n'.join(data))
            else:
                file.write(data)

    def append_data(self, filename, data):
        with open(filename, 'a') as file:
            file.write(data + '\n')

class ParentingForum(http.server.SimpleHTTPRequestHandler):
    file_manager = FileManager()
    current_user = None

    def do_GET(self):
        path = urlparse(self.path).path
        if path == '/':
            self.serve_template('templates/login.html')
        elif path == '/login':
            self.serve_template('templates/login.html')
        elif path == '/register':
            self.serve_template('templates/register.html')
        elif path == '/home':
            if self.current_user:
                self.serve_template('templates/home.html')
            else:
                self.redirect('/login')
        elif path == '/forum':
            if self.current_user:
                self.serve_template('templates/forum.html')
            else:
                self.redirect('/login')
        elif path == '/view_thread':
            if self.current_user:
                self.serve_template('templates/view_thread.html')
            else:
                self.redirect('/login')
        elif path == '/post_advice':
            if self.current_user:
                self.serve_template('templates/post_advice.html')
            else:
                self.redirect('/login')
        elif path == '/account':
            if self.current_user:
                self.serve_template('templates/account.html')
            else:
                self.redirect('/login')
        elif path == '/contact':
            self.serve_template('templates/contact.html')
        else:
            super().do_GET()

    def do_POST(self):
        path = urlparse(self.path).path
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        data = parse_qs(post_data)

        if path == '/login':
            self.authenticate(data)
        elif path == '/register':
            self.register_user(data)
        elif path == '/create_thread':
            self.create_thread(data)
        elif path == '/add_comment':
            self.add_comment(data)
        elif path == '/post_advice':
            self.post_advice(data)
        elif path == '/update_account':
            self.update_account(data)
        elif path == '/delete_account':
            self.delete_account()
        elif path == '/submit_contact':
            self.submit_contact(data)
        else:
            self.send_error(404)

    def serve_template(self, template_path):
        try:
            with open(template_path, 'r') as file:
                content = file.read()
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(content.encode('utf-8'))
        except FileNotFoundError:
            self.send_error(404)

    def authenticate(self, data):
        username = data.get('username', [''])[0]
        password = data.get('password', [''])[0]
        users = self.file_manager.read_data('users.txt')
        
        for user in users:
            if user.startswith(username + '|'):
                if user == f"{username}|{password}":
                    self.current_user = username
                    self.send_response(303)
                    self.send_header('Location', '/home')
                    self.end_headers()
                    return
        
        self.send_response(303)
        self.send_header('Location', '/login?error=1')
        self.end_headers()

    def register_user(self, data):
        username = data.get('username', [''])[0]
        password = data.get('password', [''])[0]
        users = self.file_manager.read_data('users.txt')
        
        for user in users:
            if user.startswith(username + '|'):
                self.send_response(303)
                self.send_header('Location', '/register?error=1')
                self.end_headers()
                return
        
        self.file_manager.append_data('users.txt', f"{username}|{password}")
        self.send_response(303)
        self.send_header('Location', '/login')
        self.end_headers()

    def create_thread(self, data):
        if not self.current_user:
            self.redirect('/login')
            return
            
        title = data.get('title', [''])[0]
        content = data.get('content', [''])[0]
        threads = self.file_manager.read_data('threads.txt')
        thread_id = len(threads) + 1
        
        thread_data = {
            'id': thread_id,
            'title': title,
            'content': content,
            'author': self.current_user
        }
        
        self.file_manager.append_data('threads.txt', json.dumps(thread_data))
        self.redirect('/forum')

    def add_comment(self, data):
        if not self.current_user:
            self.redirect('/login')
            return
            
        thread_id = int(data.get('thread_id', ['0'])[0])
        content = data.get('content', [''])[0]
        
        comment_data = {
            'thread_id': thread_id,
            'author': self.current_user,
            'content': content
        }
        
        self.file_manager.append_data('comments.txt', json.dumps(comment_data))
        self.redirect(f'/view_thread?id={thread_id}')

    def post_advice(self, data):
        if not self.current_user:
            self.redirect('/login')
            return
            
        title = data.get('title', [''])[0]
        content = data.get('content', [''])[0]
        
        advice_data = {
            'title': title,
            'content': content,
            'author': self.current_user
        }
        
        self.file_manager.append_data('advice.txt', json.dumps(advice_data))
        self.redirect('/home')

    def update_account(self, data):
        if not self.current_user:
            self.redirect('/login')
            return
            
        new_password = data.get('password', [''])[0]
        users = self.file_manager.read_data('users.txt')
        updated_users = []
        
        for user in users:
            if user.startswith(self.current_user + '|'):
                updated_users.append(f"{self.current_user}|{new_password}")
            else:
                updated_users.append(user)
        
        self.file_manager.write_data('users.txt', updated_users)
        self.redirect('/account')

    def delete_account(self):
        if not self.current_user:
            self.redirect('/login')
            return
            
        users = self.file_manager.read_data('users.txt')
        updated_users = [user for user in users if not user.startswith(self.current_user + '|')]
        
        self.file_manager.write_data('users.txt', updated_users)
        self.current_user = None
        self.redirect('/login')

    def submit_contact(self, data):
        name = data.get('name', [''])[0]
        email = data.get('email', [''])[0]
        message = data.get('message', [''])[0]
        
        contact_data = {
            'name': name,
            'email': email,
            'message': message
        }
        
        self.file_manager.append_data('contacts.txt', json.dumps(contact_data))
        self.redirect('/contact?success=1')

    def redirect(self, location):
        self.send_response(303)
        self.send_header('Location', location)
        self.end_headers()

def run_server():
    PORT = 8000
    with socketserver.TCPServer(("", PORT), ParentingForum) as httpd:
        print(f"Serving at port {PORT}")
        httpd.serve_forever()

if __name__ == "__main__":
    run_server()