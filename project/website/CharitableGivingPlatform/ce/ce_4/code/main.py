from flask import Flask, render_template, request, redirect, url_for, session
from user import User
from charity import Charity
from donation import Donation

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def load_users():
    users = []
    with open('users.txt', 'r') as file:
        for line in file:
            username, password = line.strip().split('|')
            users.append(User(username, password))
    return users

def load_charities():
    charities = []
    with open('charities.txt', 'r') as file:
        for line in file:
            name, mission, projects = line.strip().split('|')
            charities.append(Charity(name, mission, projects.split(',')))
    return charities

def load_donations():
    donations = []
    with open('donations.txt', 'r') as file:
        for line in file:
            username, charity_name, amount = line.strip().split('|')
            donations.append(Donation(username, charity_name, float(amount)))
    return donations

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
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    charities = load_charities()
    return render_template('dashboard.html', charities=charities)

@app.route('/charity/<charity_name>', methods=['GET', 'POST'])
def charity_details(charity_name):
    charities = load_charities()
    charity = next((c for c in charities if c.name == charity_name), None)
    if request.method == 'POST':
        amount = request.form['amount']
        donation = Donation(session['username'], charity_name, float(amount))
        donation.save()
        return redirect(url_for('dashboard'))
    return render_template('charity_details.html', charity=charity)

if __name__ == '__main__':
    app.run(port=9002, debug=False)
