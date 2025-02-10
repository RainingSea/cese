from flask import Flask, render_template, request, redirect, session
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

class Culture:
    def __init__(self, name: str, facts: list):
        self.name = name
        self.facts = facts

    def get_details(self) -> str:
        return f"{self.name}: " + ", ".join(self.facts)

class Main:
    def __init__(self):
        self.users = self.load_users()
        self.cultures = self.load_culture_facts()

    def load_users(self):
        users = {}
        if os.path.exists('users.txt'):
            with open('users.txt', 'r') as file:
                for line in file:
                    username, password = line.strip().split(',')
                    users[username] = User(username, password)
        return users

    def load_culture_facts(self):
        cultures = {}
        if os.path.exists('cultures.txt'):
            with open('cultures.txt', 'r') as file:
                for line in file:
                    culture_name, fact = line.strip().split(',')
                    if culture_name not in cultures:
                        cultures[culture_name] = Culture(culture_name, [])
                    cultures[culture_name].facts.append(fact)
        return cultures

    def register_user(self, username: str, password: str) -> bool:
        if username in self.users:
            return False
        self.users[username] = User(username, password)
        with open('users.txt', 'a') as file:
            file.write(f"{username},{password}\n")
        return True

    def login_user(self, username: str, password: str) -> bool:
        user = self.users.get(username)
        if user and user.password == password:
            session['username'] = username
            return True
        return False

    def logout_user(self) -> None:
        session.pop('username', None)

    def get_culture_facts(self) -> list:
        return self.cultures

    def bookmark_fact(self, culture_name: str) -> None:
        if 'bookmarks' not in session:
            session['bookmarks'] = []
        session['bookmarks'].append(culture_name)

    def get_bookmarked_facts(self) -> list:
        return session.get('bookmarks', [])

main_instance = Main()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if main_instance.register_user(username, password):
            return redirect('/')
    return render_template('registration.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', cultures=main_instance.get_culture_facts())

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    if main_instance.login_user(username, password):
        return redirect('/dashboard')
    return redirect('/')

@app.route('/logout')
def do_logout():
    main_instance.logout_user()
    return redirect('/')

@app.route('/culture/<culture_name>')
def culture_details(culture_name):
    culture = main_instance.get_culture_facts().get(culture_name)
    return render_template('culture_details.html', culture=culture)

@app.route('/bookmark/<culture_name>')
def bookmark(culture_name):
    main_instance.bookmark_fact(culture_name)
    return redirect('/dashboard')

@app.route('/bookmarks')
def bookmarks():
    bookmarks = main_instance.get_bookmarked_facts()
    return render_template('bookmarks.html', bookmarks=bookmarks)

if __name__ == '__main__':
    app.run(port=8612, debug=False)
