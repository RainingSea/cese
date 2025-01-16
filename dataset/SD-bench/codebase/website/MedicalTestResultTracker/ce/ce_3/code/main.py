from flask import Flask, render_template, request, redirect, url_for, session
from user import User
from test_result import TestResult
from reminder import Reminder

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def load_users():
    users = []
    with open('users.txt', 'r') as file:
        for line in file:
            username, password = line.strip().split('|')
            users.append(User(username, password))
    return users

def load_test_results():
    test_results = []
    with open('test_results.txt', 'r') as file:
        for line in file:
            user_id, test_name, result, date = line.strip().split('|')
            test_results.append(TestResult(user_id, test_name, result, date))
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
        return redirect(url_for('login'))
    return render_template('registration.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    users = load_users()
    user = next((u for u in users if u.username == session['username']), None)
    test_results = load_test_results()
    user_test_results = [tr for tr in test_results if tr.user_id == user.username]
    
    return render_template('dashboard.html', test_results=user_test_results)

@app.route('/authenticate', methods=['POST'])
def authenticate():
    username = request.form['username']
    password = request.form['password']
    users = load_users()
    user = next((u for u in users if u.username == username and u.password == password), None)
    
    if user:
        session['username'] = username
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8644, debug=False)
