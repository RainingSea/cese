from flask import Flask, render_template, request, redirect, url_for, session
from User import User
from TestResult import TestResult
from Reminder import Reminder

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def load_users():
    users = []
    with open('users.txt', 'r') as file:
        for line in file:
            username, password = line.strip().split('|')
            users.append(User(username, password))
    return users

def load_results():
    results = []
    with open('results.txt', 'r') as file:
        for line in file:
            user_id, test_name, result, date = line.strip().split('|')
            results.append(TestResult(user_id, test_name, result, date))
    return results

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
    return render_template('registration.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    user_id = session['username']
    results = load_results()
    user_results = [result for result in results if result.user_id == user_id]
    return render_template('dashboard.html', results=user_results)

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    users = load_users()
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
    app.run(port=9046, debug=False)
