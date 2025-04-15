from flask import Flask, render_template, request, redirect, session
from data_storage import UserStorage, CharityStorage, DonationStorage
from models import User, Charity, Donation
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'

user_storage = UserStorage()
charity_storage = CharityStorage()
donation_storage = DonationStorage()

users = user_storage.load_users()
charities = charity_storage.load_charities()
donations = donation_storage.load_donations()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if register_user(username, password):
            return redirect('/')
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return render_template('dashboard.html', charities=charities, contributions=get_contribution_history())
    return redirect('/')

@app.route('/charity/<charity_name>')
def charity_details(charity_name):
    charity = next((c for c in charities if c.name == charity_name), None)
    return render_template('charity_details.html', charity=charity)

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    user = login_user(username, password)
    if user:
        session['username'] = user.username
        return redirect('/dashboard')
    return redirect('/')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')

def register_user(username, password):
    if any(user.username == username for user in users):
        return False
    new_user = User(username, password)
    users.append(new_user)
    user_storage.save_user(new_user)
    return True

def login_user(username, password):
    for user in users:
        if user.username == username and user.password == password:
            return user
    return None

def get_contribution_history():
    user = next((u for u in users if u.username == session['username']), None)
    return user.get_contributions() if user else []

if __name__ == '__main__':
    app.run(port=8328, debug=False)
