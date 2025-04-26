from flask import Flask, render_template, request, redirect, session
from typing import List
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure key

class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def register(self) -> bool:
        users = app_instance.load_users()
        if any(user.username == self.username for user in users):
            return False
        app_instance.save_user(self)
        return True

    def login(self) -> bool:
        users = app_instance.load_users()
        return any(user.username == self.username and user.password == self.password for user in users)

class Charity:
    def __init__(self, name: str, mission: str, projects: str):
        self.name = name
        self.mission = mission
        self.projects = projects

    def get_details(self) -> str:
        return f"Name: {self.name}, Mission: {self.mission}, Projects: {self.projects}"

class Donation:
    def __init__(self, username: str, charity_name: str, amount: float):
        self.username = username
        self.charity_name = charity_name
        self.amount = amount

    def record_donation(self):
        app_instance.save_donation(self)

class App:
    def __init__(self):
        self.users: List[User] = []
        self.charities: List[Charity] = []
        self.donations: List[Donation] = []

    def load_users(self) -> List[User]:
        users = []
        if os.path.exists('users.txt'):
            with open('users.txt', 'r') as file:
                for line in file:
                    username, password = line.strip().split('|')
                    users.append(User(username, password))
        return users

    def load_charities(self) -> List[Charity]:
        charities = []
        if os.path.exists('charities.txt'):
            with open('charities.txt', 'r') as file:
                for line in file:
                    name, mission, projects = line.strip().split('|')
                    charities.append(Charity(name, mission, projects))
        return charities

    def load_donations(self) -> List[Donation]:
        donations = []
        if os.path.exists('donations.txt'):
            with open('donations.txt', 'r') as file:
                for line in file:
                    username, charity_name, amount = line.strip().split('|')
                    donations.append(Donation(username, charity_name, float(amount)))
        return donations

    def save_user(self, user: User):
        with open('users.txt', 'a') as file:
            file.write(f"{user.username}|{user.password}\n")
        self.users.append(user)

    def save_charity(self, charity: Charity):
        with open('charities.txt', 'a') as file:
            file.write(f"{charity.name}|{charity.mission}|{charity.projects}\n")
        self.charities.append(charity)

    def save_donation(self, donation: Donation):
        with open('donations.txt', 'a') as file:
            file.write(f"{donation.username}|{donation.charity_name}|{donation.amount}\n")
        self.donations.append(donation)

    def get_contribution_history(self, username: str):
        contributions = []
        if os.path.exists('donations.txt'):
            with open('donations.txt', 'r') as file:
                for line in file:
                    user, charity, amount = line.strip().split('|')
                    if user == username:
                        contributions.append((charity, amount))
        return contributions

    def reset_data_files(self):
        open('users.txt', 'w').close()
        open('charities.txt', 'w').close()
        open('donations.txt', 'w').close()

app_instance = App()
app_instance.reset_data_files()  # Ensure data files are clean before loading
app_instance.users = app_instance.load_users()
app_instance.charities = app_instance.load_charities()
app_instance.donations = app_instance.load_donations()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User(username, password)
        if user.login():
            session['username'] = username
            return redirect('/dashboard')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        new_user = User(username, password)
        if new_user.register():
            return redirect('/')
        else:
            return "Registration failed. Username already exists."
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect('/')
    charities = app_instance.load_charities()
    contributions = app_instance.get_contribution_history(session['username'])
    return render_template('dashboard.html', charities=charities, contributions=contributions)

@app.route('/charity/<charity_name>')
def charity_details(charity_name):
    if 'username' not in session:
        return redirect('/')
    charities = app_instance.load_charities()
    charity = next((c for c in charities if c.name == charity_name), None)
    return render_template('charity_details.html', charity=charity)

@app.route('/donate', methods=['POST'])
def donate():
    if 'username' in session:
        username = session['username']
        charity_name = request.form['charity_name']
        amount = float(request.form['amount'])
        donation = Donation(username, charity_name, amount)
        donation.record_donation()
        return redirect('/dashboard')
    return redirect('/')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(port=8138, debug=False)
