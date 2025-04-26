from flask import Flask, render_template, request, redirect, url_for, session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)

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

    def register(self, username: str, password: str) -> bool:
        if username in self.users:
            return False
        self.users[username] = password
        with open('users.txt', 'a') as file:
            file.write(f"{username}|{password}\n")
        return True

    def login(self, username: str, password: str) -> bool:
        if username in self.users and self.users[username] == password:
            return True
        return False

class CultureManager:
    def __init__(self):
        self.cultures = self.load_cultures()

    def load_cultures(self):
        cultures = {}
        if os.path.exists('cultures.txt'):
            with open('cultures.txt', 'r') as file:
                for line in file:
                    parts = line.strip().split('|')
                    cultures[parts[0]] = parts[1:]
        return cultures

    def get_cultures(self):
        return list(self.cultures.keys())

    def get_culture_details(self, culture_name: str) -> str:
        return self.cultures.get(culture_name, [])

    def bookmark_culture(self, username: str, culture_name: str) -> bool:
        with open('bookmarks.txt', 'a') as file:
            file.write(f"{username}|{culture_name}\n")
        return True

    def get_bookmarks(self, username: str):
        bookmarks = []
        if os.path.exists('bookmarks.txt'):
            with open('bookmarks.txt', 'r') as file:
                for line in file:
                    user, culture = line.strip().split('|')
                    if user == username:
                        bookmarks.append(culture)
        return bookmarks

user_manager = UserManager()
culture_manager = CultureManager()

@login_manager.user_loader
def load_user(username):
    return User(username)

class User(UserMixin):
    def __init__(self, username):
        self.id = username

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            return redirect(url_for('login'))
    return render_template('registration.html')

@app.route('/dashboard')
@login_required
def dashboard():
    cultures = culture_manager.get_cultures()
    return render_template('dashboard.html', cultures=cultures)

@app.route('/culture/<culture_name>')
@login_required
def culture_details(culture_name):
    details = culture_manager.get_culture_details(culture_name)
    return render_template('culture_details.html', culture_name=culture_name, details=details)

@app.route('/bookmark/<culture_name>')
@login_required
def bookmark(culture_name):
    user_manager.bookmark_culture(session['username'], culture_name)
    return redirect(url_for('dashboard'))

@app.route('/bookmarks')
@login_required
def bookmarks():
    user_bookmarks = culture_manager.get_bookmarks(session['username'])
    return render_template('bookmarks.html', bookmarks=user_bookmarks)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8148, debug=False)
