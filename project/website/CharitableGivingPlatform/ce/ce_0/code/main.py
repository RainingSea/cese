from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def login(self, username: str, password: str) -> bool:
        users = self.load_users()
        for user in users:
            if user.username == username and user.password == password:
                return True
        return False

    def register(self, username: str, password: str) -> bool:
        users = self.load_users()
        if any(user.username == username for user in users):
            return False
        users.append(User(username, password))
        self.save_users(users)
        return True

    def load_users(self):
        users = []
        if os.path.exists('users.txt'):
            with open('users.txt', 'r') as file:
                for line in file:
                    username, password = line.strip().split('|')
                    users.append(User(username, password))
        return users

    def save_users(self, users):
        with open('users.txt', 'w') as file:
            for user in users:
                file.write(f"{user.username}|{user.password}\n")

class Charity:
    def __init__(self, name, mission, projects):
        self.name = name
        self.mission = mission
        self.projects = projects

    def get_details(self) -> str:
        return f"Name: {self.name}, Mission: {self.mission}, Projects: {self.projects}"

    @staticmethod
    def load_charities():
        charities = []
        if os.path.exists('charities.txt'):
            with open('charities.txt', 'r') as file:
                for line in file:
                    name, mission, projects = line.strip().split('|')
                    charities.append(Charity(name, mission, projects))
        return charities

class Donation:
    def __init__(self, username, charity_name, amount):
        self.username = username
        self.charity_name = charity_name
        self.amount = amount

    def record_donation(self):
        donations = self.load_donations()
        donations.append(self)
        self.save_donations(donations)

    @staticmethod
    def load_donations():
        donations = []
        if os.path.exists('donations.txt'):
            with open('donations.txt', 'r') as file:
                for line in file:
                    username, charity_name, amount = line.strip().split('|')
                    donations.append(Donation(username, charity_name, float(amount)))
        return donations

    @staticmethod
    def save_donations(donations):
        with open('donations.txt', 'w') as file:
            for donation in donations:
                file.write(f"{donation.username}|{donation.charity_name}|{donation.amount}\n")

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User(username, password)
        if user.register(username, password):
            return redirect(url_for('login'))
        else:
            return "Registration failed. Username already exists."
    return render_template('registration.html')

@app.route('/dashboard')
def view_dashboard():
    charities = Charity.load_charities()
    return render_template('dashboard.html', charities=charities)

@app.route('/charity/<charity_name>', methods=['GET', 'POST'])
def view_charity_details(charity_name):
    charities = Charity.load_charities()
    charity = next((c for c in charities if c.name == charity_name), None)
    if request.method == 'POST':
        username = request.form['username']
        amount = float(request.form['amount'])
        donation = Donation(username, charity_name, amount)
        donation.record_donation()
        return redirect(url_for('view_dashboard'))
    return render_template('charity_details.html', charity=charity)

if __name__ == '__main__':
    app.run(port=8135, debug=False)
