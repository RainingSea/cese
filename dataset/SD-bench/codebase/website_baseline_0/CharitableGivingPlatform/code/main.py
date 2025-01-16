from flask import Flask, render_template, request, redirect, url_for, session
import os
import logging

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def save(self):
        with open('users.txt', 'a') as f:
            f.write(f"{self.username}|{self.password}\n")

class Charity:
    def __init__(self, name: str, mission: str, projects: list):
        self.name = name
        self.mission = mission
        self.projects = projects

    def save(self):
        with open('charities.txt', 'a') as f:
            f.write(f"{self.name}|{self.mission}|{'|'.join(self.projects)}\n")

class Donation:
    def __init__(self, username: str, charity_name: str, amount: float):
        self.username = username
        self.charity_name = charity_name
        self.amount = amount

    def save(self):
        with open('donations.txt', 'a') as f:
            f.write(f"{self.username}|{self.charity_name}|{self.amount}\n")

class CharitableGivingPlatform:
    def __init__(self):
        self.users = self.load_users()
        self.charities = self.load_charities()
        self.donations = self.load_donations()

    def load_users(self):
        users = []
        if os.path.exists('users.txt'):
            with open('users.txt', 'r') as f:
                for line in f:
                    username, password = line.strip().split('|')
                    users.append(User(username, password))
        logging.debug(f"Loaded users: {users}")
        return users

    def load_charities(self):
        charities = []
        if os.path.exists('charities.txt'):
            with open('charities.txt', 'r') as f:
                for line in f:
                    name, mission, projects = line.strip().split('|')
                    charities.append(Charity(name, mission, projects.split('|')))
        logging.debug(f"Loaded charities: {charities}")
        return charities

    def load_donations(self):
        donations = []
        if os.path.exists('donations.txt'):
            with open('donations.txt', 'r') as f:
                for line in f:
                    username, charity_name, amount = line.strip().split('|')
                    donations.append(Donation(username, charity_name, float(amount)))
        logging.debug(f"Loaded donations: {donations}")
        return donations

    def login(self, username: str, password: str) -> bool:
        for user in self.users:
            if user.username == username and user.password == password:
                session['username'] = username
                logging.info(f"User {username} logged in successfully.")
                return True
        logging.warning(f"Failed login attempt for user {username}.")
        return False

    def register(self, username: str, password: str) -> None:
        new_user = User(username, password)
        new_user.save()
        self.users.append(new_user)
        logging.info(f"User {username} registered successfully.")

    def view_charities(self) -> list:
        return self.charities

    def donate(self, username: str, charity_name: str, amount: float) -> None:
        new_donation = Donation(username, charity_name, amount)
        new_donation.save()
        self.donations.append(new_donation)
        logging.info(f"User {username} donated {amount} to {charity_name}.")

platform = CharitableGivingPlatform()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if platform.login(username, password):
            return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        platform.register(username, password)
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    charities = platform.view_charities()
    return render_template('dashboard.html', charities=charities)

@app.route('/charity/<charity_name>', methods=['GET', 'POST'])
def charity_details(charity_name):
    charity = next((c for c in platform.charities if c.name == charity_name), None)
    if request.method == 'POST':
        amount = float(request.form['amount'])
        platform.donate(session['username'], charity_name, amount)
        return redirect(url_for('dashboard'))
    return render_template('charity_details.html', charity=charity)

if __name__ == '__main__':
    app.run(port=8526, debug=False)
