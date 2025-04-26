from flask import Flask, render_template, request, redirect, session
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'

class UserManager:
    def __init__(self):
        self.users = self.load_users()

    def load_users(self):
        users = {}
        if os.path.exists('users.txt'):
            with open('users.txt', 'r') as file:
                for line in file:
                    username, password = line.strip().split('|')
                    users[username] = password
        return users

    def login(self, username: str, password: str) -> bool:
        if username in self.users and self.users[username] == password:
            session['username'] = username
            return True
        return False

    def register(self, username: str, password: str) -> bool:
        if username not in self.users:
            self.users[username] = password
            with open('users.txt', 'a') as file:
                file.write(f"{username}|{password}\n")
            return True
        return False

    def get_contribution_history(self, username: str) -> list:
        contributions = []
        if os.path.exists('contributions.txt'):
            with open('contributions.txt', 'r') as file:
                for line in file:
                    user, charity, amount = line.strip().split('|')
                    if user == username:
                        contributions.append((charity, amount))
        return contributions

class CharityManager:
    def __init__(self):
        self.charities = self.load_charities()

    def load_charities(self):
        charities = {}
        if os.path.exists('charities.txt'):
            with open('charities.txt', 'r') as file:
                for line in file:
                    name, mission, projects = line.strip().split('|')
                    charities[name] = {'mission': mission, 'projects': projects.split(',')}
        return charities

    def get_charities(self) -> list:
        return list(self.charities.keys())

    def get_charity_details(self, charity_name: str) -> dict:
        return self.charities.get(charity_name, {})

    def record_donation(self, username: str, charity_name: str, amount: float) -> None:
        with open('contributions.txt', 'a') as file:
            file.write(f"{username}|{charity_name}|{amount}\n")

user_manager = UserManager()
charity_manager = CharityManager()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.login(username, password):
            return redirect('/dashboard')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            return redirect('/')
    return render_template('registration.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect('/')
    charities = charity_manager.get_charities()
    contributions = user_manager.get_contribution_history(session['username'])
    return render_template('dashboard.html', charities=charities, contributions=contributions)

@app.route('/charity/<charity_name>')
def charity_details(charity_name):
    if 'username' not in session:
        return redirect('/')
    charity = charity_manager.get_charity_details(charity_name)
    return render_template('charity_details.html', charity=charity)

@app.route('/donate', methods=['POST'])
def donate():
    if 'username' not in session:
        return redirect('/')
    charity_name = request.form['charity_name']
    amount = float(request.form['amount'])
    charity_manager.record_donation(session['username'], charity_name, amount)
    return redirect('/dashboard')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(port=8137, debug=False)
