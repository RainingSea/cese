from flask import Flask, render_template, request, redirect, url_for, session
from data_manager import DataManager, User, Charity, Donation

app = Flask(__name__)
app.secret_key = 'your_secret_key'
data_manager = DataManager()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = data_manager.load_users()
        new_user = User(username, password)
        users.append(new_user)
        data_manager.save_users(users)
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    charities = data_manager.load_charities()
    donations = data_manager.load_donations()
    return render_template('dashboard.html', charities=charities, donations=donations)

@app.route('/charity/<charity_name>', methods=['GET', 'POST'])
def charity_details(charity_name):
    if request.method == 'POST':
        amount = float(request.form['amount'])
        username = session['username']
        donation = Donation(username, charity_name, amount)
        donations = data_manager.load_donations()
        donations.append(donation)
        data_manager.save_donations(donations)
        return redirect(url_for('dashboard'))
    
    charities = data_manager.load_charities()
    charity = next((c for c in charities if c.name == charity_name), None)
    return render_template('charity_details.html', charity=charity)

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    users = data_manager.load_users()
    for user in users:
        if user.username == username and user.password == password:
            session['username'] = username
            return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8595, debug=False)
