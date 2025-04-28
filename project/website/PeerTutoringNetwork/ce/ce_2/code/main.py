import os
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class Main:
    def __init__(self):
        self.user_manager = UserManager('users.txt')
        self.tutoring_request_manager = TutoringRequestManager('tutoring_requests.txt')
        self.contact_manager = ContactManager('contact_messages.txt')

    def main(self):
        app.run(port=8392, debug=False)

class UserManager:
    def __init__(self, users_file: str):
        self.users_file = users_file
        self.load_users()

    def load_users(self):
        self.users = {}
        if os.path.exists(self.users_file):
            with open(self.users_file, 'r') as file:
                for line in file:
                    username, password, email = line.strip().split(':')
                    self.users[username] = {'password': password, 'email': email}

    def register(self, username: str, password: str, email: str) -> bool:
        if username in self.users:
            return False
        with open(self.users_file, 'a') as file:
            file.write(f"{username}:{password}:{email}\n")
        self.users[username] = {'password': password, 'email': email}
        return True

    def login(self, username: str, password: str) -> bool:
        if username in self.users and self.users[username]['password'] == password:
            session['username'] = username
            return True
        return False

    def get_user_info(self, username: str) -> dict:
        return self.users.get(username, None)

class TutoringRequestManager:
    def __init__(self, requests_file: str):
        self.requests_file = requests_file
        self.load_requests()

    def load_requests(self):
        self.requests = []
        if os.path.exists(self.requests_file):
            with open(self.requests_file, 'r') as file:
                for line in file:
                    self.requests.append(line.strip())

    def request_tutoring(self, username: str, subject: str, details: str, date: str) -> bool:
        request_entry = f"{username}:{subject}:{details}:{date}\n"
        with open(self.requests_file, 'a') as file:
            file.write(request_entry)
        self.requests.append(request_entry.strip())
        return True

    def cancel_request(self, username: str) -> bool:
        # This method will be a placeholder for future implementation
        return False

class ContactManager:
    def __init__(self, messages_file: str):
        self.messages_file = messages_file

    def send_message(self, name: str, email: str, message: str) -> bool:
        with open(self.messages_file, 'a') as file:
            file.write(f"{name}:{email}:{message}\n")
        return True

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']
    if main_instance.user_manager.register(username, password, email):
        return redirect(url_for('login'))
    return "Registration failed", 400

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

if __name__ == '__main__':
    main_instance = Main()
    main_instance.main()