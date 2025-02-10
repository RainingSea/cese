from flask import Flask, render_template, request, redirect, url_for
from typing import List

app = Flask(__name__)

class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

class Charity:
    def __init__(self, id: int, name: str, mission: str, ongoing_projects: str):
        self.id = id
        self.name = name
        self.mission = mission
        self.ongoing_projects = ongoing_projects

def load_users() -> List[User]:
    users = []
    with open('users.txt', 'r') as file:
        for line in file:
            username, password = line.strip().split('|')
            users.append(User(username, password))
    return users

def load_charities() -> List[Charity]:
    charities = []
    with open('charities.txt', 'r') as file:
        for line in file:
            id, name, mission, ongoing_projects = line.strip().split('|')
            charities.append(Charity(int(id), name, mission, ongoing_projects))
    return charities

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = load_users()
        for user in users:
            if user.username == username and user.password == password:
                return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        with open('users.txt', 'a') as file:
            file.write(f"{username}|{password}\n")
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    charities = load_charities()
    return render_template('dashboard.html', charities=charities)

@app.route('/charity/<int:charity_id>')
def charity_details(charity_id: int):
    charities = load_charities()
    charity = next((c for c in charities if c.id == charity_id), None)
    return render_template('charity_details.html', charity=charity)

@app.route('/donate/<int:charity_id>', methods=['POST'])
def donate(charity_id: int):
    amount = request.form['amount']
    # Here you can handle the donation logic (e.g., store in a database)
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(port=8594, debug=False)
