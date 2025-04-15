from flask import Flask, render_template, request, redirect, session
from data_storage import UserStorage, CharityStorage, DonationStorage
from user import User
from charity import Charity
from donation import Donation
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'

user_storage = UserStorage()
charity_storage = CharityStorage()
donation_storage = DonationStorage()

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
        charities = get_charities()
        return render_template('dashboard.html', charities=charities)
    return redirect('/')

@app.route('/charity/<charity_name>', methods=['GET', 'POST'])
def charity_details_route(charity_name):
    charity = charity_details(charity_name)
    if request.method == 'POST':
        amount = request.form['amount']
        if donate_to_charity(session['username'], charity, amount):
            return redirect('/dashboard')
    return render_template('charity_details.html', charity=charity)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')

def register_user(username, password):
    users = user_storage.load_users()
    for user in users:
        if user.username == username:
            return False
    new_user = User(username, password)
    user_storage.save_user(new_user)
    return True

def get_charities():
    return charity_storage.load_charities()

def charity_details(charity_name):
    charities = charity_storage.load_charities()
    for charity in charities:
        if charity.name == charity_name:
            return charity
    return None

def donate_to_charity(username, charity, amount):
    if charity and amount:
        donation = Donation(username, charity, float(amount), datetime.now().strftime("%Y-%m-%d"))
        donation_storage.save_donation(donation)
        return True
    return False

if __name__ == '__main__':
    app.run(port=8330, debug=False)
