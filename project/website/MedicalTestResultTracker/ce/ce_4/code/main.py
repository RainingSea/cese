from flask import Flask, render_template, request, redirect, url_for, session
from user import User
from test_result import TestResult
from reminder import Reminder

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
    
    test_results = TestResult.load_all(session['username'])
    return render_template('dashboard.html', test_results=test_results)

@app.route('/trends')
def trends():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    return render_template('trends.html')

@app.route('/reminders', methods=['GET', 'POST'])
def reminders():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        test_name = request.form['test_name']
        date = request.form['date']
        reminder = Reminder(session['username'], test_name, date)
        reminder.save()
    
    reminders = Reminder.load_all(session['username'])
    return render_template('reminders.html', reminders=reminders)

if __name__ == '__main__':
    app.run(port=9050, debug=False)
