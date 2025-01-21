from flask import Flask, render_template, request, redirect, url_for, session
from user import User
from test_result import TestResult

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
    return render_template('registration.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    username = session['username']
    if request.method == 'POST':
        test_name = request.form['test_name']
        result = request.form['result']
        date = request.form['date']
        test_result = TestResult(username, test_name, result, date)
        test_result.save()
    
    return render_template('dashboard.html', username=username)

@app.route('/history')
def history():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    username = session['username']
    test_results = TestResult.load_results(username)
    return render_template('history.html', results=test_results)

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    user = User()
    users = user.load_users()
    
    for u in users:
        if u[0] == username and u[1] == password:
            session['username'] = username
            return redirect(url_for('dashboard'))
    
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=9048, debug=False)
