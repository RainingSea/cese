from flask import Flask, render_template, request, redirect, url_for, session
from DataManager import DataManager, User

app = Flask(__name__)
app.secret_key = 'your_secret_key'
data_manager = DataManager()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        tips = data_manager.load_tips()
        articles = data_manager.load_articles()
        return render_template('dashboard.html', username=session['username'], tips=tips, articles=articles)
    return redirect(url_for('login'))

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    if data_manager.register(username, password):
        return redirect(url_for('login'))
    return "Registration failed. Username may already exist."

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    if data_manager.login(username, password):
        session['username'] = username
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/submit_tip', methods=['POST'])
def submit_tip():
    if 'username' in session:
        tip = request.form['tip']
        data_manager.save_tip(session['username'], tip)
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8955, debug=False)
