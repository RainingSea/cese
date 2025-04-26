from flask import Flask, render_template, request, redirect, url_for, session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin):
    def __init__(self, username, password):
        self.username = username
        self.password = password

class UserManager:
    def __init__(self, users_file: str):
        self.users_file = users_file
        self.load_users()

    def load_users(self):
        self.users = {}
        if os.path.exists(self.users_file):
            with open(self.users_file, 'r') as file:
                for line in file:
                    username, password = line.strip().split('|')
                    self.users[username] = password

    def register(self, username: str, password: str) -> bool:
        if username in self.users:
            return False
        self.users[username] = password
        with open(self.users_file, 'a') as file:
            file.write(f"{username}|{password}\n")
        return True

    def login(self, username: str, password: str) -> bool:
        if username in self.users and self.users[username] == password:
            return True
        return False

class TestResultManager:
    def __init__(self, results_file: str):
        self.results_file = results_file
        self.load_results()

    def load_results(self):
        self.results = []
        if os.path.exists(self.results_file):
            with open(self.results_file, 'r') as file:
                for line in file:
                    user_id, test_name, result, date = line.strip().split('|')
                    self.results.append((user_id, test_name, result, date))

    def add_test_result(self, user_id: str, test_name: str, result: str, date: str) -> bool:
        self.results.append((user_id, test_name, result, date))
        with open(self.results_file, 'a') as file:
            file.write(f"{user_id}|{test_name}|{result}|{date}\n")
        return True

    def get_test_results(self, user_id: str) -> list:
        return [result for result in self.results if result[0] == user_id]

class ReminderManager:
    def __init__(self, reminders_file: str):
        self.reminders_file = reminders_file
        self.load_reminders()

    def load_reminders(self):
        self.reminders = []
        if os.path.exists(self.reminders_file):
            with open(self.reminders_file, 'r') as file:
                for line in file:
                    user_id, reminder_text, date = line.strip().split('|')
                    self.reminders.append((user_id, reminder_text, date))

    def set_reminder(self, user_id: str, reminder_text: str, date: str) -> bool:
        self.reminders.append((user_id, reminder_text, date))
        with open(self.reminders_file, 'a') as file:
            file.write(f"{user_id}|{reminder_text}|{date}\n")
        return True

    def get_reminders(self, user_id: str) -> list:
        return [reminder for reminder in self.reminders if reminder[0] == user_id]

user_manager = UserManager('users.txt')
test_result_manager = TestResultManager('test_results.txt')
reminder_manager = ReminderManager('reminders.txt')

@login_manager.user_loader
def load_user(username):
    return User(username, user_manager.users[username])

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.login(username, password):
            user = User(username, password)
            login_user(user)
            return redirect(url_for('test_results'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            return redirect(url_for('login'))
    return render_template('registration.html')

@app.route('/test_results', methods=['GET', 'POST'])
@login_required
def test_results():
    if request.method == 'POST':
        test_name = request.form['test_name']
        result = request.form['result']
        date = datetime.now().strftime('%Y-%m-%d')
        test_result_manager.add_test_result(session['user_id'], test_name, result, date)
    results = test_result_manager.get_test_results(session['user_id'])
    return render_template('test_results.html', results=results)

@app.route('/reminders', methods=['GET', 'POST'])
@login_required
def reminders():
    if request.method == 'POST':
        reminder_text = request.form['reminder_text']
        date = request.form['date']
        reminder_manager.set_reminder(session['user_id'], reminder_text, date)
    reminders = reminder_manager.get_reminders(session['user_id'])
    return render_template('reminders.html', reminders=reminders)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8182, debug=False)
