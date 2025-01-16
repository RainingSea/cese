from flask import Flask, render_template, request, redirect, url_for, session, flash
from typing import List
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

class TestResult:
    def __init__(self, username: str, test_name: str, result: float, date: str):
        self.username = username
        self.test_name = test_name
        self.result = result
        self.date = date

class Reminder:
    def __init__(self, username: str, reminder: str, date: str):
        self.username = username
        self.reminder = reminder
        self.date = date

def load_users() -> List[User]:
    users = []
    with open('users.txt', 'r') as file:
        for line in file:
            username, password = line.strip().split('|')
            users.append(User(username, password))
    return users

def load_test_results() -> List[TestResult]:
    test_results = []
    with open('test_results.txt', 'r') as file:
        for line in file:
            username, test_name, result, date = line.strip().split('|')
            test_results.append(TestResult(username, test_name, float(result), date))
    return test_results

def load_reminders() -> List[Reminder]:
    reminders = []
    with open('reminders.txt', 'r') as file:
        for line in file:
            username, reminder, date = line.strip().split('|')
            reminders.append(Reminder(username, reminder, date))
    return reminders

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = load_users()
        for user in users:
            if user.username == username and user.password == password:
                session['username'] = username
                return redirect(url_for('dashboard'))
        flash('Invalid username or password', 'danger')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = load_users()
        if any(user.username == username for user in users):
            flash('Username already exists. Please choose a different one.', 'danger')
            return render_template('register.html')
        with open('users.txt', 'a') as file:
            file.write(f"{username}|{password}\n")
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    username = session.get('username')
    if not username:
        return redirect(url_for('login'))
    return render_template('dashboard.html', username=username)

@app.route('/history')
def history():
    username = session.get('username')
    if not username:
        return redirect(url_for('login'))
    test_results = load_test_results()
    user_results = [result for result in test_results if result.username == username]
    return render_template('history.html', results=user_results)

@app.route('/test_result/<int:index>')
def test_result_details(index):
    username = session.get('username')
    if not username:
        return redirect(url_for('login'))
    test_results = load_test_results()
    user_results = [result for result in test_results if result.username == username]
    if index < len(user_results):
        result = user_results[index]
        return render_template('test_result_details.html', result=result)
    return redirect(url_for('history'))

@app.route('/add_test_result', methods=['GET', 'POST'])
def add_test_result():
    username = session.get('username')
    if not username:
        return redirect(url_for('login'))
    if request.method == 'POST':
        test_name = request.form['test_name']
        result = request.form['result']
        date = request.form['date']
        with open('test_results.txt', 'a') as file:
            file.write(f"{username}|{test_name}|{result}|{date}\n")
        return redirect(url_for('history'))
    return render_template('add_test_result.html')

@app.route('/reminders', methods=['GET', 'POST'])
def reminders():
    username = session.get('username')
    if not username:
        return redirect(url_for('login'))
    if request.method == 'POST':
        reminder_text = request.form['reminder']
        date = request.form['date']
        with open('reminders.txt', 'a') as file:
            file.write(f"{username}|{reminder_text}|{date}\n")
        return redirect(url_for('reminders'))
    
    user_reminders = load_reminders()
    user_reminders = [reminder for reminder in user_reminders if reminder.username == username]
    return render_template('reminders.html', reminders=user_reminders)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/view_trends')
def view_trends():
    username = session.get('username')
    if not username:
        return redirect(url_for('login'))
    test_results = load_test_results()
    user_results = [result for result in test_results if result.username == username]
    
    if not user_results:
        flash('No test results available for trend analysis.', 'info')
        return redirect(url_for('dashboard'))

    test_names = [result.test_name for result in user_results]
    results = [result.result for result in user_results]

    plt.figure(figsize=(10, 5))
    plt.plot(test_names, results, marker='o')
    plt.title('Test Results Trend')
    plt.xlabel('Test Name')
    plt.ylabel('Result')
    plt.xticks(rotation=45)
    
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    plt.close()

    return render_template('view_trends.html', plot_url=plot_url)

if __name__ == '__main__':
    app.run(port=8538, debug=False)
