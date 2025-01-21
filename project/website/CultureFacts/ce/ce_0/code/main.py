from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

class Culture:
    def __init__(self, name: str, facts: str):
        self.name = name
        self.facts = facts

def load_users():
    users = []
    if os.path.exists('users.txt'):
        with open('users.txt', 'r') as file:
            for line in file:
                username, password = line.strip().split('|')
                users.append(User(username, password))
    return users

def load_cultures():
    cultures = []
    if os.path.exists('cultures.txt'):
        with open('cultures.txt', 'r') as file:
            for line in file:
                name, facts = line.strip().split('|')
                cultures.append(Culture(name, facts))
    return cultures

def save_user(username: str, password: str):
    with open('users.txt', 'a') as file:
        file.write(f"{username}|{password}\n")

def save_bookmark(username: str, culture_name: str):
    with open(f"{username}_bookmarks.txt", 'a') as file:
        file.write(f"{culture_name}\n")

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        save_user(username, password)
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/dashboard', methods=['GET'])
def dashboard():
    cultures = load_cultures()
    return render_template('dashboard.html', cultures=cultures)

@app.route('/culture/<string:culture_name>', methods=['GET'])
def culture_details(culture_name):
    cultures = load_cultures()
    culture = next((c for c in cultures if c.name == culture_name), None)
    return render_template('culture_details.html', culture=culture)

@app.route('/bookmarks', methods=['GET'])
def bookmarks():
    username = session.get('username')
    bookmarks = []
    if username and os.path.exists(f"{username}_bookmarks.txt"):
        with open(f"{username}_bookmarks.txt", 'r') as file:
            bookmarks = [line.strip() for line in file]
    return render_template('bookmarks.html', bookmarks=bookmarks)

if __name__ == '__main__':
    app.run(port=9016, debug=False)
