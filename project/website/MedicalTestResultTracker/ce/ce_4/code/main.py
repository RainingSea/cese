from flask import Flask, render_template, request, redirect, url_for, session
import json
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def save(self):
        with open('users.txt', 'a') as f:
            f.write(f"{self.username}|{self.password}\n")

class TestResult:
    def __init__(self, date: str, result: str, type: str):
        self.date = date
        self.result = result
        self.type = type

    def save(self):
        with open('test_results.txt', 'a') as f:
            f.write(f"{self.date}|{self.result}|{self.type}\n")

class Reminder:
    def __init__(self, test_type: str, date: str):
        self.test_type = test_type
        self.date = date

    def save(self):
        with open('reminders.txt', 'a') as f:
            f.write(f"{self.test_type}|{self.date}\n")

class App:
    def __init__(self):
        self.users = self.load_users()
        self.test_results = self.load_test_results()
        self.reminders = self.load_reminders()

    def load_users(self):
        users = []
        if os.path.exists('users.txt'):
            with open('users.txt', 'r') as f:
                for line in f.readlines():
                    username, password = line.strip().split('|')
                    users.append(User(username, password))
        return users

    def load_test_results(self):
        test_results = []
        if os.path.exists('test_results.txt'):
            with open('test_results.txt', 'r') as f:
                for line in f.readlines():
                    date, result, type = line.strip().split('|')
                    test_results.append(TestResult(date, result, type))
        return test_results

    def load_reminders(self):
        reminders = []
        if os.path.exists('reminders.txt'):
            with open('reminders.txt', 'r') as f:
                for line in f.readlines():
                    test_type, date = line.strip().split('|')
                    reminders.append(Reminder(test_type, date))
        return reminders

    def register(self, username: str, password: str) -> bool:
        if any(user.username == username for user in self.users):
            return False
        new_user = User(username, password)
        new_user.save()
        self.users.append(new_user)
        return True

    def login(self, username: str, password: str) -> bool:
        return any(user.username == username and user.password == password for user in self.users)

    def add_test_result(self, date: str, result: str, type: str) -> None:
        new_result = TestResult(date, result, type)
        new_result.save()
        self.test_results.append(new_result)

    def set_reminder(self, test_type: str, date: str) -> None:
        new_reminder = Reminder(test_type, date)
        new_reminder.save()
        self.reminders.append(new_reminder)

    def view_trends(self) -> list:
        return self.test_results

app_instance = App()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if app_instance.login(username, password):
            session['username'] = username
            return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if app_instance.register(username, password):
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', username=session.get('username'))

if __name__ == '__main__':
    app.run(port=8708, debug=False)
