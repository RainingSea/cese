from flask import Flask, render_template, request, redirect, url_for, session
from user import User
from test_result import TestResult
from reminder import Reminder
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def load_users(filename):
    users = []
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            for line in file:
                username, password = line.strip().split('|')
                users.append(User(username, password))
    return users

def load_test_results(filename):
    results = []
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            for line in file:
                user, test_name, result, date = line.strip().split('|')
                results.append(TestResult(user, test_name, float(result), date))
    return results

def load_reminders(filename):
    reminders = []
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            for line in file:
                user, message, date = line.strip().split('|')
                reminders.append(Reminder(user, message, date))
    return reminders

users = load_users('users.txt')
test_results = load_test_results('test_results.txt')
reminders = load_reminders('reminders.txt')

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        new_user = User(username, password)
        new_user.save_to_file('users.txt')
        users.append(new_user)
        return redirect(url_for('login'))
    return render_template('registration.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if request.method == 'POST':
        user = session['username']
        test_name = request.form['test_name']
        result = request.form['result']
        date = request.form['date']
        new_result = TestResult(user, test_name, float(result), date)
        new_result.save_to_file('test_results.txt')
        test_results.append(new_result)
    return render_template('dashboard.html', results=test_results)

@app.route('/reminders', methods=['GET', 'POST'])
def reminders_page():
    if request.method == 'POST':
        user = session['username']
        message = request.form['message']
        date = request.form['date']
        new_reminder = Reminder(user, message, date)
        new_reminder.save_to_file('reminders.txt')
        reminders.append(new_reminder)
    return render_template('reminders.html', reminders=reminders)

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    for user in users:
        if user.username == username and user.password == password:
            session['username'] = username
            return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8641, debug=False)
