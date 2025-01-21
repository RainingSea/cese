from flask import Flask, render_template, request, redirect, url_for, session
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

    @staticmethod
    def load(username: str):
        with open('users.txt', 'r') as f:
            for line in f:
                user_data = line.strip().split('|')
                if user_data[0] == username:
                    return User(user_data[0], user_data[1])
        return None

class TestResult:
    def __init__(self, user: User, test_name: str, result: float, date: str):
        self.user = user
        self.test_name = test_name
        self.result = result
        self.date = date

    def save(self):
        with open('test_results.txt', 'a') as f:
            f.write(f"{self.user.username}|{self.test_name}|{self.result}|{self.date}\n")

    @staticmethod
    def load(user: User):
        results = []
        with open('test_results.txt', 'r') as f:
            for line in f:
                result_data = line.strip().split('|')
                if result_data[0] == user.username:
                    results.append((result_data[1], float(result_data[2]), result_data[3]))
        return results

class Reminder:
    def __init__(self, user: User, test_name: str, date: str):
        self.user = user
        self.test_name = test_name
        self.date = date

    def save(self):
        with open('reminders.txt', 'a') as f:
            f.write(f"{self.user.username}|{self.test_name}|{self.date}\n")

    @staticmethod
    def load(user: User):
        reminders = []
        with open('reminders.txt', 'r') as f:
            for line in f:
                reminder_data = line.strip().split('|')
                if reminder_data[0] == user.username:
                    reminders.append((reminder_data[1], reminder_data[2]))
        return reminders

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.load(username)
        if user and user.password == password:
            session['username'] = username
            return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        new_user = User(username, password)
        new_user.save()
        return redirect(url_for('login'))
    return render_template('registration.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    user = User.load(session['username'])
    test_results = TestResult.load(user)
    reminders = Reminder.load(user)
    return render_template('dashboard.html', test_results=test_results, reminders=reminders)

if __name__ == '__main__':
    app.run(port=9047, debug=False)
