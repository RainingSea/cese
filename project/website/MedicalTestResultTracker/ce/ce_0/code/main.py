from flask import Flask, render_template, request, redirect, session
from flask_session import Session
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

class UserManager:
    def __init__(self):
        self.users = self.load_users()

    def load_users(self):
        if not os.path.exists('users.txt'):
            return []
        with open('users.txt', 'r') as file:
            return [line.strip().split('|') for line in file.readlines()]

    def register(self, username: str, password: str) -> bool:
        for user in self.users:
            if user[0] == username:
                return False
        self.users.append([username, password])
        with open('users.txt', 'a') as file:
            file.write(f"{username}|{password}\n")
        return True

    def login(self, username: str, password: str) -> bool:
        for user in self.users:
            if user[0] == username and user[1] == password:
                return True
        return False

class TestResultManager:
    def __init__(self):
        self.test_results = self.load_test_results()

    def load_test_results(self):
        if not os.path.exists('test_results.txt'):
            return []
        with open('test_results.txt', 'r') as file:
            return [line.strip().split('|') for line in file.readlines()]

    def add_test_result(self, user_id: str, result: str) -> bool:
        self.test_results.append([user_id, result])
        with open('test_results.txt', 'a') as file:
            file.write(f"{user_id}|{result}\n")
        return True

    def get_test_results(self, user_id: str) -> list:
        return [result for result in self.test_results if result[0] == user_id]

    def get_trends(self, user_id: str) -> str:
        results = self.get_test_results(user_id)
        # Placeholder for trend calculation logic
        return "Trend data for user"

class ReminderManager:
    def __init__(self):
        self.reminders = self.load_reminders()

    def load_reminders(self):
        if not os.path.exists('reminders.txt'):
            return []
        with open('reminders.txt', 'r') as file:
            return [line.strip().split('|') for line in file.readlines()]

    def set_reminder(self, user_id: str, reminder: str) -> bool:
        self.reminders.append([user_id, reminder])
        with open('reminders.txt', 'a') as file:
            file.write(f"{user_id}|{reminder}\n")
        return True

    def get_reminders(self, user_id: str) -> list:
        return [reminder for reminder in self.reminders if reminder[0] == user_id]

@app.route('/', methods=['GET', 'POST'])
def login():
    user_manager = UserManager()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.login(username, password):
            session['username'] = username
            return redirect('/dashboard')
        else:
            return "Invalid credentials"
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    user_manager = UserManager()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            return redirect('/')
        else:
            return "Username already exists"
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run(port=8346, debug=False)
