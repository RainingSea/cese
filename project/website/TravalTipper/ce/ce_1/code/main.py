from flask import Flask, render_template, request, redirect, url_for, session
from auth_service import AuthService
from tip_service import TipService

app = Flask(__name__)
app.secret_key = 'your_secret_key'

auth_service = AuthService()
tip_service = TipService()

@app.route('/')
def home():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if auth_service.login(username, password):
            session['username'] = username
            return redirect(url_for('dashboard'))
        return render_template('login.html', error='Invalid credentials')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if auth_service.register(username, password):
            return redirect(url_for('login'))
        return render_template('register.html', error='Username already exists')
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    saved_tips = tip_service.get_saved_tips(session['username'])
    return render_template('dashboard.html', username=session['username'], saved_tips=saved_tips)

@app.route('/get_tips', methods=['POST'])
def get_tips():
    if 'username' not in session:
        return redirect(url_for('login'))
    destination = request.form['destination']
    interests = request.form.getlist('interests')
    tips = tip_service.get_tips(destination, interests)
    return render_template('tips.html', tips=tips, destination=destination)

@app.route('/save_tip', methods=['POST'])
def save_tip():
    if 'username' not in session:
        return redirect(url_for('login'))
    tip_id = request.form['tip_id']
    tip_service.save_tip(session['username'], tip_id)
    return redirect(url_for('dashboard'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8065, debug=False)
