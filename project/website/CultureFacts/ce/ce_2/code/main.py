from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)

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
        return self.users.get(username) == password

    def load_users(self) -> None:
        try:
            with open('data/users.txt', 'r') as file:
                for line in file:
                    username, password = line.strip().split('|')
                    self.users[username] = password
        except FileNotFoundError:
            pass

    def save_users(self) -> None:
        with open('data/users.txt', 'w') as file:
            for username, password in self.users.items():
                file.write(f"{username}|{password}\n")


class CultureManager:
    def __init__(self):
        self.cultures = {}
        self.load_cultures()

    def load_cultures(self) -> None:
        try:
            with open('data/cultures.txt', 'r') as file:
                for line in file:
                    name, details = line.strip().split('|')
                    self.cultures[name] = details
        except FileNotFoundError:
            pass

    def get_culture_details(self, culture_name: str) -> str:
        return self.cultures.get(culture_name, "Culture not found.")

    def search_cultures(self, query: str) -> list:
        return [name for name in self.cultures if query.lower() in name.lower()]


class BookmarkManager:
    def __init__(self):
        self.bookmarks = {}
        self.load_bookmarks()

    def add_bookmark(self, username: str, culture_name: str) -> None:
        if username not in self.bookmarks:
            self.bookmarks[username] = []
        if culture_name not in self.bookmarks[username]:
            self.bookmarks[username].append(culture_name)
            self.save_bookmarks()

    def remove_bookmark(self, username: str, culture_name: str) -> None:
        if username in self.bookmarks and culture_name in self.bookmarks[username]:
            self.bookmarks[username].remove(culture_name)
            self.save_bookmarks()

    def load_bookmarks(self) -> None:
        try:
            with open('data/bookmarks.txt', 'r') as file:
                for line in file:
                    username, cultures = line.strip().split('|')
                    self.bookmarks[username] = cultures.split(',')
        except FileNotFoundError:
            pass

    def save_bookmarks(self) -> None:
        with open('data/bookmarks.txt', 'w') as file:
            for username, cultures in self.bookmarks.items():
                file.write(f"{username}|{','.join(cultures)}\n")


user_manager = UserManager()
culture_manager = CultureManager()
bookmark_manager = BookmarkManager()


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.login(username, password):
            return redirect(url_for('dashboard'))
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/dashboard')
def dashboard():
    cultures = culture_manager.cultures.keys()
    return render_template('dashboard.html', cultures=cultures)


@app.route('/culture/<culture_name>')
def culture_details(culture_name):
    details = culture_manager.get_culture_details(culture_name)
    return render_template('culture_details.html', culture_name=culture_name, details=details)


@app.route('/bookmarks')
def bookmarks():
    # Assuming a logged-in user 'user1' for demo purposes
    user = 'user1'
    user_bookmarks = bookmark_manager.bookmarks.get(user, [])
    return render_template('bookmarks.html', bookmarks=user_bookmarks)


if __name__ == '__main__':
    app.run(port=8313, debug=False)
