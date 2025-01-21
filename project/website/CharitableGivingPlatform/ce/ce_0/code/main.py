from flask import Flask, render_template, request, redirect, url_for, session
from user import User
from charity import Charity
from donation import Donation

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Load data from files
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
            id, name, mission, projects = line.strip().split('|')
            charities.append(Charity(id, name, mission, projects))
    return charities

def load_donations():
    donations = []
    with open('donations.txt', 'r') as file:
        for line in file:
            user_id, charity_id, amount = line.strip().split('|')
            donations.append(Donation(user_id, charity_id, float(amount)))
    return donations

users = load_users()
charities = load_charities()
donations = load_donations()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        for user in users:
            if user.username == username and user.password == password:
                session['username'] = username
                return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        new_user = User(username, password)
        new_user.save()
        users.append(new_user)
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', charities=charities)

@app.route('/charity/<charity_id>')
def charity_details(charity_id):
    charity = next((c for c in charities if c.id == charity_id), None)
    return render_template('charity_details.html', charity=charity)

@app.route('/donate/<charity_id>', methods=['POST'])
def donate(charity_id):
    amount = float(request.form['amount'])
    donation = Donation(session['username'], charity_id, amount)
    donation.save()
    donations.append(donation)
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(port=8998, debug=False)
