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
        users = []
        if os.path.exists('users.txt'):
            with open('users.txt', 'r') as file:
                for line in file:
                    username, password = line.strip().split('|')
                    users.append({'username': username, 'password': password})
        return users

    def register(self, username: str, password: str) -> bool:
        if any(user['username'] == username for user in self.users):
            return False
        self.users.append({'username': username, 'password': password})
        with open('users.txt', 'a') as file:
            file.write(f"{username}|{password}\n")
        return True

    def login(self, username: str, password: str) -> bool:
        return any(user['username'] == username and user['password'] == password for user in self.users)

class TestResultManager:
    def __init__(self):
        self.test_results = self.load_test_results()

    def load_test_results(self):
        test_results = []
        if os.path.exists('test_results.txt'):
            with open('test_results.txt', 'r') as file:
                for line in file:
                    user_id, result = line.strip().split('|')
                    test_results.append({'user_id': user_id, 'result': result})
        return test_results

    def add_test_result(self, user_id: str, result: str) -> bool:
        self.test_results.append({'user_id': user_id, 'result': result})
        with open('test_results.txt', 'a') as file:
            file.write(f"{user_id}|{result}\n")
        return True

    def get_test_results(self, user_id: str) -> list:
        return [result for result in self.test_results if result['user_id'] == user_id]

    def get_trends(self, user_id: str) -> list:
        # Placeholder for trend analysis logic
        return self.get_test_results(user_id)

class ReminderManager:
    def __init__(self):
        self.reminders = self.load_reminders()

    def load_reminders(self):
        reminders = []
        if os.path.exists('reminders.txt'):
            with open('reminders.txt', 'r') as file:
                for line in file:
                    user_id, reminder = line.strip().split('|')
                    reminders.append({'user_id': user_id, 'reminder': reminder})
        return reminders

    def set_reminder(self, user_id: str, reminder: str) -> bool:
        self.reminders.append({'user_id': user_id, 'reminder': reminder})
        with open('reminders.txt', 'a') as file:
            file.write(f"{user_id}|{reminder}\n")
        return True

    def get_reminders(self, user_id: str) -> list:
        return [reminder for reminder in self.reminders if reminder['user_id'] == user_id]

user_manager = UserManager()
test_result_manager = TestResultManager()
reminder_manager = ReminderManager()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.login(username, password):
            session['username'] = username
            return redirect('/dashboard')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            return redirect('/')
    return render_template('registration.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect('/')
    user_id = session['username']
    test_results = test_result_manager.get_test_results(user_id)
    reminders = reminder_manager.get_reminders(user_id)
    return render_template('dashboard.html', test_results=test_results, reminders=reminders)

if __name__ == '__main__':
    app.run(port=8184, debug=False)
