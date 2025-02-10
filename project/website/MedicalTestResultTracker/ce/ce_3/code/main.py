from flask import Flask, render_template, request, redirect, session
from user import User
from test_result import TestResult
from reminder import Reminder
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'

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
    return render_template('registration.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'username' not in session:
        return redirect('/')
    
    username = session['username']
    if request.method == 'POST':
        test_name = request.form['test_name']
        result_value = float(request.form['result_value'])
        date = request.form['date']
        test_result = TestResult(test_name, result_value, date)
        test_result.save(username)
    
    test_results = TestResult.load_history(username)
    return render_template('dashboard.html', results=test_results)

@app.route('/reminders', methods=['GET', 'POST'])
def reminders():
    if 'username' not in session:
        return redirect('/')
    
    username = session['username']
    if request.method == 'POST':
        test_name = request.form['test_name']
        reminder_date = request.form['reminder_date']
        reminder = Reminder(test_name, reminder_date)
        reminder.save(username)
    
    reminders_list = Reminder.load(username)
    return render_template('reminders.html', reminders=reminders_list)

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    user = User.load(username)
    if user and user.password == password:
        session['username'] = username
        return redirect('/dashboard')
    return redirect('/')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(port=8707, debug=False)
