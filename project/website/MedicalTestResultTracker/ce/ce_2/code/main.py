from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime
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
    def __init__(self, user: str, test_name: str, result: str, date: str):
        self.user = user
        self.test_name = test_name
        self.result = result
        self.date = date

    def save(self):
        with open('test_results.txt', 'a') as f:
            f.write(f"{self.user}|{self.test_name}|{self.result}|{self.date}\n")

class Reminder:
    def __init__(self, user: str, message: str, date: str):
        self.user = user
        self.message = message
        self.date = date

    def save(self):
        with open('reminders.txt', 'a') as f:
            f.write(f"{self.user}|{self.message}|{self.date}\n")

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User(username, password)
        user.save()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        test_name = request.form['test_name']
        result = request.form['result']
        date = request.form['date']
        test_result = TestResult(session['username'], test_name, result, date)
        test_result.save()
        
        reminder_message = request.form.get('reminder_message')
        reminder_date = request.form.get('reminder_date')
        if reminder_message and reminder_date:
            reminder = Reminder(session['username'], reminder_message, reminder_date)
            reminder.save()

    return render_template('dashboard.html', username=session['username'], test_results=view_test_results(session['username']), reminders=view_reminders(session['username']))

@app.route('/do_login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    with open('users.txt', 'r') as f:
        users = f.readlines()
        for user in users:
            u, p = user.strip().split('|')
            if u == username and p == password:
                session['username'] = username
                return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

def view_test_results(user: str):
    results = []
    with open('test_results.txt', 'r') as f:
        for line in f:
            u, test_name, result, date = line.strip().split('|')
            if u == user:
                results.append((test_name, result, date))
    return results

def view_reminders(user: str):
    reminders = []
    with open('reminders.txt', 'r') as f:
        for line in f:
            u, message, date = line.strip().split('|')
            if u == user:
                reminders.append((message, date))
    return reminders

if __name__ == '__main__':
    app.run(port=8706, debug=False)
