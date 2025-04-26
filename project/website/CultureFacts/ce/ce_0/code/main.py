from flask import Flask, render_template, request, redirect, session, url_for
from flask_session import Session

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
        try:
            with open('users.txt', 'r') as file:
                for line in file:
                    username, password = line.strip().split('|')
                    self.users[username] = password
        except FileNotFoundError:
            pass

    def save_users(self) -> None:
        with open('users.txt', 'w') as file:
            for username, password in self.users.items():
                file.write(f"{username}|{password}\n")

class CultureManager:
    def __init__(self):
        self.cultures = {}
        self.load_cultures()

    def load_cultures(self) -> None:
        try:
            with open('cultures.txt', 'r') as file:
                for line in file:
                    culture_name, details = line.strip().split('|', 1)
                    self.cultures[culture_name] = details
        except FileNotFoundError:
            pass

    def get_culture_details(self, culture_name: str) -> str:
        return self.cultures.get(culture_name, "Culture not found.")

    def search_cultures(self, query: str) -> list:
        return [name for name in self.cultures if query.lower() in name.lower()]

    def bookmark_culture(self, username: str, culture_name: str) -> None:
        if 'bookmarks' not in session:
            session['bookmarks'] = {}
        if username not in session['bookmarks']:
            session['bookmarks'][username] = []
        if culture_name not in session['bookmarks'][username]:
            session['bookmarks'][username].append(culture_name)

    def get_bookmarks(self, username: str) -> list:
        return session.get('bookmarks', {}).get(username, [])

user_manager = UserManager()
culture_manager = CultureManager()

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
        else:
            return "Username already exists."
    return render_template('registration.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', cultures=culture_manager.cultures)

@app.route('/culture/<culture_name>')
def culture_details(culture_name):
    details = culture_manager.get_culture_details(culture_name)
    return render_template('culture_details.html', details=details)

@app.route('/bookmark/<culture_name>')
def bookmark(culture_name):
    if 'username' in session:
        culture_manager.bookmark_culture(session['username'], culture_name)
    return redirect(url_for('dashboard'))

@app.route('/bookmarks')
def bookmarks():
    if 'username' in session:
        bookmarked_cultures = culture_manager.get_bookmarks(session['username'])
        return render_template('bookmarks.html', bookmarks=bookmarked_cultures)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8147, debug=False)
