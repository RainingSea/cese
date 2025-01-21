from flask import Flask, render_template, request, redirect, url_for, session
from bcrypt import hashpw, gensalt, checkpw
import os
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = hashpw(password.encode('utf-8'), gensalt()).decode('utf-8')

    def save(self):
        with open('users.txt', 'a') as f:
            f.write(f"{self.username}|{self.password}\n")

    @staticmethod
    def load(username: str):
        with open('users.txt', 'r') as f:
            for line in f:
                user, password = line.strip().split('|')
                if user == username:
                    return User(user, password)
        return None

class TestResult:
    def __init__(self, user: str, test_name: str, result: float, date: str):
        self.user = user
        self.test_name = test_name
        self.result = result
        self.date = date

    def save(self):
        with open('test_results.txt', 'a') as f:
            f.write(f"{self.user}|{self.test_name}|{self.result}|{self.date}\n")

    @staticmethod
    def load(user: str):
        results = []
        with open('test_results.txt', 'r') as f:
            for line in f:
                u, test_name, result, date = line.strip().split('|')
                if u == user:
                    results.append(TestResult(u, test_name, float(result), date))
        return results

class Reminder:
    def __init__(self, user: str, test_name: str, date: str):
        self.user = user
        self.test_name = test_name
        self.date = date

    def save(self):
        with open('reminders.txt', 'a') as f:
            f.write(f"{self.user}|{self.test_name}|{self.date}\n")

    @staticmethod
    def load(user: str):
        reminders = []
        with open('reminders.txt', 'r') as f:
            for line in f:
                u, test_name, date = line.strip().split('|')
                if u == user:
                    reminders.append(Reminder(u, test_name, date))
        return reminders

class App:
    @staticmethod
    def register(username: str, password: str):
        user = User(username, password)
        user.save()

    @staticmethod
    def login(username: str, password: str) -> bool:
        user = User.load(username)
        if user and checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            return True
        return False

    @staticmethod
    def add_test_result(user: str, test_name: str, result: float, date: str):
        test_result = TestResult(user, test_name, result, date)
        test_result.save()

    @staticmethod
    def get_test_results(user: str):
        return TestResult.load(user)

    @staticmethod
    def set_reminder(user: str, test_name: str, date: str):
        reminder = Reminder(user, test_name, date)
        reminder.save()

    @staticmethod
    def get_reminders(user: str):
        return Reminder.load(user)

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if App.login(username, password):
            session['username'] = username
            return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        App.register(username, password)
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    user = session['username']
    if request.method == 'POST':
        test_name = request.form['test_name']
        result = float(request.form['result'])
        date = request.form['date']
        App.add_test_result(user, test_name, result, date)

    test_results = App.get_test_results(user)
    return render_template('dashboard.html', test_results=test_results)

@app.route('/reminders', methods=['GET', 'POST'])
def reminders():
    if 'username' not in session:
        return redirect(url_for('login'))

    user = session['username']
    if request.method == 'POST':
        test_name = request.form['test_name']
        date = request.form['date']
        App.set_reminder(user, test_name, date)

    reminders = App.get_reminders(user)
    return render_template('reminders.html', reminders=reminders)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=9049, debug=False)
