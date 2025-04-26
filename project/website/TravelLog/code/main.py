from flask import Flask, render_template, request, redirect, session, url_for
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'

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

class EntryManager:
    def __init__(self):
        self.entries = []
        self.load_entries()

    def create_entry(self, username: str, destination: str, dates: str, activities: str, photos: str, reflections: str) -> None:
        entry_id = len(self.entries) + 1
        entry = {
            'id': entry_id,
            'username': username,
            'destination': destination,
            'dates': dates,
            'activities': activities,
            'photos': photos,
            'reflections': reflections
        }
        self.entries.append(entry)
        self.save_entries()

    def load_entries(self) -> None:
        if os.path.exists('entries.txt'):
            with open('entries.txt', 'r') as file:
                for line in file:
                    entry_data = line.strip().split('|')
                    entry = {
                        'id': int(entry_data[0]),
                        'username': entry_data[1],
                        'destination': entry_data[2],
                        'dates': entry_data[3],
                        'activities': entry_data[4],
                        'photos': entry_data[5],
                        'reflections': entry_data[6]
                    }
                    self.entries.append(entry)

    def save_entries(self) -> None:
        with open('entries.txt', 'w') as file:
            for entry in self.entries:
                file.write(f"{entry['id']}|{entry['username']}|{entry['destination']}|{entry['dates']}|{entry['activities']}|{entry['photos']}|{entry['reflections']}\n")

    def edit_entry(self, entry_id: int, updated_data: dict) -> bool:
        for entry in self.entries:
            if entry['id'] == entry_id:
                entry.update(updated_data)
                self.save_entries()
                return True
        return False

    def delete_entry(self, entry_id: int) -> bool:
        for entry in self.entries:
            if entry['id'] == entry_id:
                self.entries.remove(entry)
                self.save_entries()
                return True
        return False

    def search_entries(self, keyword: str) -> list:
        results = [entry for entry in self.entries if keyword.lower() in entry['destination'].lower()]
        return results if results else []

    def view_entries(self) -> list:
        return self.entries

user_manager = UserManager()
entry_manager = EntryManager()

@app.route('/')
def login_page():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            return redirect(url_for('login_page'))
        else:
            return "Registration failed. Username already exists."
    return render_template('registration.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    if user_manager.login(username, password):
        return redirect(url_for('entry_creation'))
    return "Login failed. Invalid credentials."

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login_page'))

@app.route('/entry_creation', methods=['GET', 'POST'])
def entry_creation():
    if 'username' not in session:
        return redirect(url_for('login_page'))
    if request.method == 'POST':
        destination = request.form['destination']
        dates = request.form['dates']
        activities = request.form['activities']
        photos = request.form['photos']
        reflections = request.form['reflections']
        entry_manager.create_entry(session['username'], destination, dates, activities, photos, reflections)
        return redirect(url_for('entry_display'))
    return render_template('entry_creation.html')

@app.route('/entry_display')
def entry_display():
    if 'username' not in session:
        return redirect(url_for('login_page'))
    entries = entry_manager.view_entries()
    return render_template('entry_display.html', entries=entries)

@app.route('/edit_entry/<int:entry_id>', methods=['GET', 'POST'])
def edit_entry(entry_id):
    if 'username' not in session:
        return redirect(url_for('login_page'))
    entry = next((entry for entry in entry_manager.view_entries() if entry['id'] == entry_id), None)
    if request.method == 'POST':
        updated_data = {
            'destination': request.form['destination'],
            'dates': request.form['dates'],
            'activities': request.form['activities'],
            'photos': request.form['photos'],
            'reflections': request.form['reflections']
        }
        if entry_manager.edit_entry(entry_id, updated_data):
            return redirect(url_for('entry_display'))
        return "Edit failed."
    return render_template('edit_entry.html', entry=entry)

@app.route('/delete_entry/<int:entry_id>', methods=['POST'])
def delete_entry(entry_id):
    if entry_manager.delete_entry(entry_id):
        return redirect(url_for('entry_display'))
    return "Delete failed."

if __name__ == '__main__':
    app.run(port=8269, debug=False)
