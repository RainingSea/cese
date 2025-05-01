from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)

class Charity:
    def __init__(self, id, name, mission, projects):
        self.id = id
        self.name = name
        self.mission = mission
        self.projects = projects

class Donation:
    def __init__(self, username, charity_id, amount, timestamp):
        self.username = username
        self.charity_id = charity_id
        self.amount = amount
        self.timestamp = timestamp

class CharitableGivingPlatform:
    @staticmethod
    def login(username, password):
        with open('users.txt', 'r') as f:
            for line in f:
                stored_user, stored_pass = line.strip().split('|')
                if username == stored_user and password == stored_pass:
                    return True
        return False

    @staticmethod
    def register(username, password):
        with open('users.txt', 'a+') as f:
            f.seek(0)
            for line in f:
                stored_user, _ = line.strip().split('|')
                if username == stored_user:
                    return False
            f.write(f"{username}|{password}\n")
        return True

    @staticmethod
    def get_charities():
        charities = []
        with open('charities.txt', 'r') as f:
            for line in f:
                id, name, mission, projects = line.strip().split('|')
                charities.append(Charity(id, name, mission, projects))
        return charities

    @staticmethod
    def get_charity_details(charity_id):
        with open('charities.txt', 'r') as f:
            for line in f:
                id, name, mission, projects = line.strip().split('|')
                if id == charity_id:
                    return Charity(id, name, mission, projects)
        return None

    @staticmethod
    def make_donation(username, charity_id, amount):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open('donations.txt', 'a') as f:
            f.write(f"{username}|{charity_id}|{amount}|{timestamp}\n")
        return True

    @staticmethod
    def get_user_donations(username):
        donations = []
        with open('donations.txt', 'r') as f:
            for line in f:
                user, charity_id, amount, timestamp = line.strip().split('|')
                if user == username:
                    donations.append(Donation(user, charity_id, amount, timestamp))
        return donations

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if CharitableGivingPlatform.login(username, password):
            return redirect(url_for('dashboard', username=username))
        return render_template('login.html', error="Invalid credentials")
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if CharitableGivingPlatform.register(username, password):
            return redirect(url_for('dashboard', username=username))
        return render_template('register.html', error="Username already exists")
    return render_template('register.html')

@app.route('/dashboard/<username>')
def dashboard(username):
    charities = CharitableGivingPlatform.get_charities()
    donations = CharitableGivingPlatform.get_user_donations(username)
    return render_template('dashboard.html', username=username, charities=charities, donations=donations)

@app.route('/charity/<id>/<username>')
def charity(id, username):
    charity = CharitableGivingPlatform.get_charity_details(id)
    return render_template('charity.html', username=username, charity=charity)

@app.route('/donate/<username>', methods=['POST'])
def donate(username):
    charity_id = request.form['charity_id']
    amount = request.form['amount']
    CharitableGivingPlatform.make_donation(username, charity_id, amount)
    return redirect(url_for('dashboard', username=username))

@app.route('/logout')
def logout():
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8565, debug=False)
