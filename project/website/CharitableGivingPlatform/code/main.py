from flask import Flask, render_template, request, redirect, session, url_for
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def register(self, username: str, password: str):
        with open('users.txt', 'a') as f:
            f.write(f"{username}|{password}\n")

    def login(self, username: str, password: str) -> bool:
        users = load_users()
        return any(user.username == username and user.password == password for user in users)

class Charity:
    def __init__(self, name: str, mission: str, ongoing_projects: str):
        self.name = name
        self.mission = mission
        self.ongoing_projects = ongoing_projects

    def getDetails(self) -> str:
        return f"Name: {self.name}, Mission: {self.mission}, Ongoing Projects: {self.ongoing_projects}"

class Contribution:
    def __init__(self, username: str, charityName: str, amount: float):
        self.username = username
        self.charityName = charityName
        self.amount = amount

    def recordContribution(self, username: str, charityName: str, amount: float):
        with open('contributions.txt', 'a') as f:
            f.write(f"{username}|{charityName}|{amount}\n")

def load_users():
    users = []
    if os.path.exists('users.txt'):
        with open('users.txt', 'r') as f:
            for line in f:
                username, password = line.strip().split('|')
                users.append(User(username, password))
    return users

def load_charities():
    charities = []
    if os.path.exists('charities.txt'):
        with open('charities.txt', 'r') as f:
            for line in f:
                name, mission, ongoing_projects = line.strip().split('|')
                charities.append(Charity(name, mission, ongoing_projects))
    return charities

def record_donation(username: str, charityName: str, amount: float):
    contributions = load_contributions()
    if amount > 0 and not any(c.charityName == charityName and c.username == username for c in contributions):
        contribution = Contribution(username, charityName, amount)
        contribution.recordContribution(username, charityName, amount)

def load_contributions():
    contributions = []
    if os.path.exists('contributions.txt'):
        with open('contributions.txt', 'r') as f:
            for line in f:
                username, charityName, amount = line.strip().split('|')
                contributions.append(Contribution(username, charityName, float(amount)))
    return contributions

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User(username, password)
        user.register(username, password)
        return redirect(url_for('login'))
    return render_template('registration.html')

@app.route('/dashboard', methods=['GET'])
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    charities = load_charities()
    contributions = load_contributions()
    return render_template('dashboard.html', charities=charities, contributions=contributions)

@app.route('/charity/<charity_name>', methods=['GET', 'POST'])
def charity_details(charity_name):
    if request.method == 'POST':
        amount = float(request.form['amount'])
        record_donation(session['username'], charity_name, amount)
        return redirect(url_for('dashboard'))
    charities = load_charities()
    charity = next((c for c in charities if c.name == charity_name), None)
    return render_template('charity_details.html', charity=charity)

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    user = User(username, password)
    if user.login(username, password):
        session['username'] = username
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8377, debug=False)
