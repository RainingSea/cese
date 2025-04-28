from flask import Flask, render_template, request, redirect, session
from flask_session import Session
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

class UserManager:
    def __init__(self):
        self.users = {}
        self.load_users()

    def register(self, username: str, password: str) -> bool:
        if username in self.users:
            return False
        self.users[username] = password
        self.save_users()
        return True

    def login(self, username: str, password: str) -> bool:
        if username in self.users and self.users[username] == password:
            session['username'] = username
            return True
        return False

    def load_users(self) -> None:
        if os.path.exists('users.txt'):
            with open('users.txt', 'r') as file:
                for line in file:
                    username, password = line.strip().split('|')
                    self.users[username] = password

    def save_users(self) -> None:
        with open('users.txt', 'w') as file:
            for username, password in self.users.items():
                file.write(f"{username}|{password}\n")

class CultureManager:
    def __init__(self):
        self.cultures = {}
        self.load_cultures()

    def load_cultures(self) -> None:
        if os.path.exists('cultures.txt'):
            with open('cultures.txt', 'r') as file:
                for line in file:
                    name, details = line.strip().split('|')
                    self.cultures[name] = details

    def get_culture_details(self, culture_name: str) -> str:
        return self.cultures.get(culture_name, "Culture not found.")

    def search_cultures(self, query: str) -> list:
        return [name for name in self.cultures if query.lower() in name.lower()]

class BookmarkManager:
    def __init__(self):
        self.bookmarks = []
        self.load_bookmarks()

    def add_bookmark(self, culture_name: str) -> None:
        if culture_name not in self.bookmarks:
            self.bookmarks.append(culture_name)
            self.save_bookmarks()

    def remove_bookmark(self, culture_name: str) -> None:
        if culture_name in self.bookmarks:
            self.bookmarks.remove(culture_name)
            self.save_bookmarks()

    def load_bookmarks(self) -> None:
        if os.path.exists('bookmarks.txt'):
            with open('bookmarks.txt', 'r') as file:
                self.bookmarks = [line.strip() for line in file]

    def save_bookmarks(self) -> None:
        with open('bookmarks.txt', 'w') as file:
            for culture in self.bookmarks:
                file.write(f"{culture}\n")

user_manager = UserManager()
culture_manager = CultureManager()
bookmark_manager = BookmarkManager()

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
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', cultures=culture_manager.cultures)

@app.route('/culture/<name>')
def culture_details(name):
    details = culture_manager.get_culture_details(name)
    return render_template('culture_details.html', name=name, details=details)

@app.route('/bookmarks')
def bookmarks():
    return render_template('bookmarks.html', bookmarks=bookmark_manager.bookmarks)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(port=8311, debug=False)
