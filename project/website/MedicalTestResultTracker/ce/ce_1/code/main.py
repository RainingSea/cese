from flask import Flask, render_template, request, redirect, url_for, session
from user import User
from test_result import TestResult
from reminder import Reminder
from trend import Trend
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User()
        if user.register(username, password):
            return redirect(url_for('login'))
    return render_template('registration.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    username = session['username']
    test_result = TestResult()
    reminder = Reminder()

    if request.method == 'POST':
        if 'result' in request.form:
            date = request.form['date']
            result = float(request.form['result'])
            test_result.add_result(username, date, result)
        elif 'reminder' in request.form:
            date = request.form['reminder_date']
            description = request.form['reminder_description']
            reminder.set_reminder(username, date, description)

    results = test_result.get_results(username)
    reminders = reminder.get_reminders(username)
    return render_template('dashboard.html', results=results, reminders=reminders)

@app.route('/history')
def history():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    username = session['username']
    test_result = TestResult()
    results = test_result.get_results(username)
    trend = Trend()
    trend.plot_trends(results)
    return render_template('history.html', results=results)

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    user = User()
    if user.login(username, password):
        session['username'] = username
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8705, debug=False)
