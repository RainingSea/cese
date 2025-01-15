from flask import Flask, render_template, request, redirect, session
from user import User
from test_result import TestResult
from reminder import Reminder

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def load_users():
    users = {}
    try:
        with open('users.txt', 'r') as file:
            for line in file:
                username, password = line.strip().split('|')
                users[username] = password
    except FileNotFoundError:
        pass
    return users

def load_test_results():
    test_results = {}
    try:
        with open('test_results.txt', 'r') as file:
            for line in file:
                user, test_name, result, date = line.strip().split('|')
                if user not in test_results:
                    test_results[user] = []
                test_results[user].append(TestResult(user, test_name, float(result), date))
    except FileNotFoundError:
        pass
    return test_results

users = load_users()
test_results = load_test_results()

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            session['username'] = username
            return redirect('/dashboard')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username not in users:
            users[username] = password
            with open('users.txt', 'a') as file:
                file.write(f"{username}|{password}\n")
            return redirect('/login')
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        username = session['username']
        user_test_results = test_results.get(username, [])
        return render_template('dashboard.html', test_results=user_test_results)
    return redirect('/login')

@app.route('/history')
def history():
    if 'username' in session:
        username = session['username']
        user_test_results = test_results.get(username, [])
        return render_template('history.html', test_results=user_test_results)
    return redirect('/login')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/login')

if __name__ == '__main__':
    app.run(port=8643, debug=False)
