from flask import Flask, render_template, request, redirect, session
from user import User
from test_result import TestResult
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Load users from file
def load_users():
    users = {}
    if os.path.exists('users.txt'):
        with open('users.txt', 'r') as file:
            for line in file:
                username, password = line.strip().split('|')
                users[username] = password
    return users

# Load test results from file
def load_test_results():
    test_results = {}
    if os.path.exists('test_results.txt'):
        with open('test_results.txt', 'r') as file:
            for line in file:
                user_id, test_name, result_value, date = line.strip().split('|')
                if user_id not in test_results:
                    test_results[user_id] = []
                test_results[user_id].append((test_name, result_value, date))
    return test_results

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
        return redirect('/')
    return render_template('register.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'username' not in session:
        return redirect('/')
    
    if request.method == 'POST':
        test_name = request.form['test_name']
        result_value = request.form['result_value']
        date = request.form['date']
        test_result = TestResult(session['username'], test_name, result_value, date)
        test_result.save()
    
    return render_template('dashboard.html', username=session['username'])

@app.route('/login', methods=['POST'])
def do_login():
    users = load_users()
    username = request.form['username']
    password = request.form['password']
    
    if username in users and users[username] == password:
        session['username'] = username
        return redirect('/dashboard')
    return redirect('/')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(port=8645, debug=False)
