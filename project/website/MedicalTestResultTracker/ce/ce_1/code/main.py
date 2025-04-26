from flask import Flask, render_template, request, redirect, url_for, session
from user_manager import UserManager
from test_result_manager import TestResultManager
from reminder_manager import ReminderManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'

user_manager = UserManager()
test_result_manager = TestResultManager()
reminder_manager = ReminderManager()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            return redirect(url_for('login'))
    return render_template('registration.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if request.method == 'POST':
        if 'username' in session:
            test_name = request.form['test_name']
            result = request.form['result']
            date = request.form['date']
            test_result_manager.add_test_result(session['username'], test_name, result, date)
    return render_template('dashboard.html', test_results=test_result_manager.get_test_results(session['username']))

@app.route('/reminders', methods=['GET', 'POST'])
def reminders():
    if request.method == 'POST':
        reminder_text = request.form['reminder_text']
        date_time = request.form['date_time']
        reminder_manager.set_reminder(session['username'], reminder_text, date_time)
    return render_template('reminders.html', reminders=reminder_manager.get_reminders(session['username']))

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    if user_manager.login(username, password):
        session['username'] = username
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8183, debug=False)
