from flask import Flask, render_template, request, redirect, url_for, session
from user import User
from charity import Charity
from donation import Donation
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def load_users():
    """Load users from the users.txt file."""
    if not os.path.exists('users.txt'):
        return []
    users = []
    with open('users.txt', 'r') as file:
        for line in file:
            username, password = line.strip().split('|')
            users.append(User(username, password))
    return users

def load_charities():
    """Load charities from the charities.txt file."""
    if not os.path.exists('charities.txt'):
        return []
    charities = []
    with open('charities.txt', 'r') as file:
        for line in file:
            name, mission, ongoing_projects = line.strip().split('|')
            charities.append(Charity(name, mission, ongoing_projects.split(',')))
    return charities

def load_donations():
    """Load donations from the donations.txt file."""
    if not os.path.exists('donations.txt'):
        return []
    donations = []
    with open('donations.txt', 'r') as file:
        for line in file:
            username, charity_name, amount, date = line.strip().split('|')
            donations.append(Donation(username, charity_name, float(amount), date))
    return donations

@app.route('/', methods=['GET', 'POST'])
def login():
    """Handle user login."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = load_users()
        for user in users:
            if user.username == username and user.password == password:
                session['username'] = username
                return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Handle user registration."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User(username, password)
        user.save_to_file()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    """Display the dashboard with available charities."""
    charities = load_charities()
    donations = load_donations()
    return render_template('dashboard.html', charities=charities, donations=donations)

@app.route('/charity/<charity_name>', methods=['GET', 'POST'])
def charity_details(charity_name):
    """Display charity details and handle donations."""
    charities = load_charities()
    charity = next((c for c in charities if c.name == charity_name), None)
    if request.method == 'POST':
        amount = request.form['amount']
        donation = Donation(session['username'], charity_name, float(amount), '2023-10-01')
        donation.save_to_file()
        return redirect(url_for('dashboard'))
    return render_template('charity_details.html', charity=charity)

@app.route('/logout')
def logout():
    """Handle user logout."""
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/contribution_history')
def contribution_history():
    """Display the contribution history of the logged-in user."""
    if 'username' not in session:
        return redirect(url_for('login'))
    
    username = session['username']
    donations = load_donations()
    user_donations = [donation for donation in donations if donation.username == username]
    
    return render_template('contribution_history.html', donations=user_donations)

if __name__ == '__main__':
    app.run(port=9003, debug=False)
