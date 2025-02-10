from flask import Flask, render_template, request, redirect, url_for, session
from UserManager import UserManager
from ResultManager import ResultManager
from ReminderManager import ReminderManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'

user_manager = UserManager()
result_manager = ResultManager()
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
        else:
            return "Username already exists."
    return render_template('register.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if request.method == 'POST':
        date = request.form['date']
        test_name = request.form['test_name']
        result = request.form['result']
        test_result = TestResult(date, test_name, result)
        result_manager.add_result(test_result)
    results = result_manager.load_results()
    return render_template('dashboard.html', results=results)

@app.route('/history')
def history():
    results = result_manager.load_results()
    return render_template('history.html', results=results)

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    if user_manager.login(username, password):
        session['username'] = username
        return redirect(url_for('dashboard'))
    return "Invalid credentials."

if __name__ == '__main__':
    app.run(port=8704, debug=False)
