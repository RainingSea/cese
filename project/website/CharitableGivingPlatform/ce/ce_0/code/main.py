from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash
import datetime

app = Flask(__name__)
app.secret_key = 'dev_key_for_demo_only'

class FileStorage:
    @staticmethod
    def read_users():
        users = {}
        try:
            with open('users.txt', 'r') as f:
                for line in f:
                    username, password = line.strip().split(':')
                    users[username] = password
        except FileNotFoundError:
            pass
        return users

    @staticmethod
    def write_user(username, password):
        with open('users.txt', 'a') as f:
            f.write(f"{username}:{password}\n")

    @staticmethod
    def read_charities():
        charities = []
        try:
            with open('charities.txt', 'r') as f:
                for line in f:
                    parts = line.strip().split(':')
                    charities.append({
                        'id': parts[0],
                        'name': parts[1],
                        'mission': parts[2],
                        'projects': parts[3]
                    })
        except FileNotFoundError:
            pass
        return charities

    @staticmethod
    def read_donations():
        donations = []
        try:
            with open('donations.txt', 'r') as f:
                for line in f:
                    parts = line.strip().split(':')
                    donations.append({
                        'username': parts[0],
                        'charity_id': parts[1],
                        'amount': float(parts[2]),
                        'timestamp': parts[3]
                    })
        except FileNotFoundError:
            pass
        return donations

    @staticmethod
    def write_donation(username, charity_id, amount):
        timestamp = datetime.datetime.now().isoformat()
        with open('donations.txt', 'a') as f:
            f.write(f"{username}:{charity_id}:{amount}:{timestamp}\n")

class CharitableApp:
    def __init__(self):
        self.storage = FileStorage()
        self.current_user = None

    def login(self, username, password):
        users = self.storage.read_users()
        if username in users and users[username] == password:
            self.current_user = username
            return True
        return False

    def register(self, username, password):
        users = self.storage.read_users()
        if username in users:
            return False
        self.storage.write_user(username, password)
        return True

    def get_charities(self):
        return self.storage.read_charities()

    def get_charity_details(self, charity_id):
        charities = self.storage.read_charities()
        for charity in charities:
            if charity['id'] == charity_id:
                return charity
        return None

    def make_donation(self, charity_id, amount):
        if not self.current_user:
            return False
        self.storage.write_donation(self.current_user, charity_id, amount)
        return True

    def get_user_donations(self, username):
        donations = self.storage.read_donations()
        return [d for d in donations if d['username'] == username]

    def logout(self):
        self.current_user = None

app_instance = CharitableApp()

@app.route('/')
def home():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if app_instance.login(username, password):
            session['username'] = username
            return redirect(url_for('dashboard'))
        return render_template('login.html', error='Invalid credentials')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if app_instance.register(username, password):
            return redirect(url_for('login'))
        return render_template('register.html', error='Username already exists')
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    charities = app_instance.get_charities()
    donations = app_instance.get_user_donations(session['username'])
    return render_template('dashboard.html', 
                         username=session['username'],
                         charities=charities,
                         donations=donations)

@app.route('/charity/<charity_id>', methods=['GET', 'POST'])
def charity(charity_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    
    charity = app_instance.get_charity_details(charity_id)
    if not charity:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        amount = float(request.form['amount'])
        app_instance.make_donation(charity_id, amount)
        return redirect(url_for('dashboard'))
    
    return render_template('charity.html', charity=charity)

@app.route('/logout')
def logout():
    app_instance.logout()
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8564, debug=False)
