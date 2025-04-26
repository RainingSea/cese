from flask import Flask, render_template, request, redirect, session
from flask_session import Session
from user_manager import UserManager
from test_result_manager import TestResultManager
from reminder_manager import ReminderManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

user_manager = UserManager('users.txt')
test_result_manager = TestResultManager('test_results.txt')
reminder_manager = ReminderManager('reminders.txt')

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.login(username, password):
            session['username'] = username
            return redirect('/dashboard')
        else:
            return render_template('login.html', error='Invalid credentials')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        registration_success = user_manager.register(username, password)
        if registration_success:
            return redirect('/')
        else:
            return render_template('registration.html', error='Username already taken')
    return render_template('registration.html')

@app.route('/dashboard')
def dashboard():
    username = session.get('username')
    if username:
        test_results = test_result_manager.get_test_results(username)
        reminders = reminder_manager.get_reminders(username)
        return render_template('dashboard.html', test_results=test_results, reminders=reminders)
    return redirect('/')

@app.route('/test_result', methods=['GET', 'POST'])
def test_result_input():
    username = session.get('username')
    if username is None:
        return redirect('/')
    if request.method == 'POST':
        result = request.form['result']
        test_result_manager.add_test_result(username, result)
        return redirect('/dashboard')
    return render_template('test_result_input.html')

@app.route('/reminder', methods=['GET', 'POST'])
def reminder_settings():
    username = session.get('username')
    if username is None:
        return redirect('/')
    if request.method == 'POST':
        reminder_text = request.form['reminder']
        date_time = request.form['date_time']
        reminder_manager.set_reminder(username, reminder_text, date_time)
        return redirect('/dashboard')
    return render_template('reminder_settings.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(port=8185, debug=False)
