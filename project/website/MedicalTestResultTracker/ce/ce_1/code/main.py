from flask import Flask, render_template, request, redirect, url_for, session
from user_manager import UserManager
from test_result_manager import TestResultManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'

user_manager = UserManager('users.txt')
test_result_manager = TestResultManager('test_results.txt')

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
        test_name = request.form['test_name']
        date = request.form['date']
        result = request.form['result']
        test_result_manager.add_test_result(session['username'], test_name, date, result)
    test_results = test_result_manager.get_test_results(session['username'])
    return render_template('test_results.html', test_results=test_results)

@app.route('/trends')
def trends():
    trends_data = test_result_manager.get_trends(session['username'])
    return render_template('trends.html', trends=trends_data)

@app.route('/reminders')
def reminders():
    return render_template('reminders.html')

@app.route('/history')
def history():
    test_results = test_result_manager.get_test_results(session['username'])
    return render_template('history.html', test_results=test_results)

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    if user_manager.login(username, password):
        session['username'] = username
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8347, debug=False)
