from flask import Flask, render_template, request, redirect, url_for, session
from charitable_platform import CharitableGivingPlatform

app = Flask(__name__)
app.secret_key = 'dev_secret_key'
platform = CharitableGivingPlatform()

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
        if platform.login_user(username, password):
            session['username'] = username
            return redirect(url_for('dashboard'))
        return render_template('login.html', error="Invalid credentials")
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if platform.register_user(username, password):
            return redirect(url_for('login'))
        return render_template('register.html', error="Username already exists")
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    username = session['username']
    charities = platform.get_charities()
    donations = platform.get_user_donations(username)
    return render_template('dashboard.html', 
                         username=username,
                         charities=charities,
                         donations=donations)

@app.route('/charity/<charity_id>', methods=['GET', 'POST'])
def charity(charity_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        amount = request.form['amount']
        if platform.make_donation(session['username'], charity_id, amount):
            return redirect(url_for('dashboard'))
        return render_template('charity.html', 
                             charity=platform.get_charity_details(charity_id),
                             error="Invalid donation amount")
    
    charity = platform.get_charity_details(charity_id)
    if not charity:
        return redirect(url_for('dashboard'))
    return render_template('charity.html', charity=charity)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8566, debug=False)
