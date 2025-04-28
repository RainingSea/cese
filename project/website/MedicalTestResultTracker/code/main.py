from flask import Flask, render_template, request, redirect, url_for, session
from user_manager import UserManager
from test_result_manager import TestResultManager
from reminder_manager import ReminderManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'

user_manager = UserManager('users.txt')
test_result_manager = TestResultManager('test_results.txt')
reminder_manager = ReminderManager('reminders.txt')

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
        else:
            return "Username already exists"
    return render_template('registration.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    username = session['username']
    if request.method == 'POST':
        result = request.form['result']
        test_result_manager.add_result(username, result)
        reminder = request.form['reminder']
        reminder_manager.set_reminder(username, reminder)

    results = test_result_manager.get_results(username)
    reminders = reminder_manager.get_reminders(username)
    trends = test_result_manager.get_trends(username)
    return render_template('dashboard.html', results=results, reminders=reminders, trends=trends)

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

@app.route('/view_test_result_history', methods=['GET'])
def view_test_result_history():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    username = session['username']
    results = test_result_manager.get_results(username)
    return render_template('test_result_history.html', results=results)

if __name__ == '__main__':
    app.run(port=8349, debug=False)
