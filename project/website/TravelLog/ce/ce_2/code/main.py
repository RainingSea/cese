from flask import Flask, render_template, request, redirect, url_for, session
import json
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def register(self) -> bool:
        users = self.load_users()
        if self.username in users:
            return False
        users[self.username] = self.password
        self.save_users(users)
        return True

    def login(self) -> bool:
        users = self.load_users()
        return users.get(self.username) == self.password

    @staticmethod
    def load_users() -> dict:
        if not os.path.exists('users.txt'):
            return {}
        with open('users.txt', 'r') as file:
            users = {}
            for line in file:
                username, password = line.strip().split('|')
                users[username] = password
            return users

    @staticmethod
    def save_users(users: dict):
        with open('users.txt', 'w') as file:
            for username, password in users.items():
                file.write(f"{username}|{password}\n")

class JournalEntry:
    def __init__(self, destination: str, dates: str, activities: str, photos: list, reflections: str):
        self.destination = destination
        self.dates = dates
        self.activities = activities
        self.photos = photos
        self.reflections = reflections

    def save(self) -> bool:
        entries = self.load_entries()
        entry_id = len(entries) + 1
        entries[entry_id] = self.__dict__
        self.save_entries(entries)
        return True

    def edit(self, entry_id: int) -> bool:
        entries = self.load_entries()
        if entry_id in entries:
            entries[entry_id] = self.__dict__
            self.save_entries(entries)
            return True
        return False

    def delete(self, entry_id: int) -> bool:
        entries = self.load_entries()
        if entry_id in entries:
            del entries[entry_id]
            self.save_entries(entries)
            return True
        return False

    @staticmethod
    def load_entries() -> dict:
        if not os.path.exists('entries.txt'):
            return {}
        with open('entries.txt', 'r') as file:
            entries = {}
            for line in file:
                entry_id, data = line.strip().split('|', 1)
                entries[int(entry_id)] = json.loads(data)
            return entries

    @staticmethod
    def save_entries(entries: dict):
        with open('entries.txt', 'w') as file:
            for entry_id, data in entries.items():
                file.write(f"{entry_id}|{json.dumps(data)}\n")

class TravelLog:
    def create_entry(self, destination: str, dates: str, activities: str, photos: list, reflections: str) -> bool:
        entry = JournalEntry(destination, dates, activities, photos, reflections)
        return entry.save()

    def view_entries(self) -> list:
        return JournalEntry.load_entries()

    def search_entries(self, query: str) -> list:
        entries = self.view_entries()
        return [entry for entry in entries.values() if query in entry['destination']]

    def share_entry(self, entry_id: int) -> str:
        entries = self.view_entries()
        return json.dumps(entries.get(entry_id, {}))

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User(username, password)
        if user.login():
            session['username'] = username
            return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User(username, password)
        if user.register():
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    travel_log = TravelLog()
    if request.method == 'POST':
        destination = request.form['destination']
        dates = request.form['dates']
        activities = request.form['activities']
        photos = request.form.getlist('photos')
        reflections = request.form['reflections']
        travel_log.create_entry(destination, dates, activities, photos, reflections)

    entries = travel_log.view_entries()
    return render_template('dashboard.html', entries=entries)

if __name__ == '__main__':
    app.run(port=8268, debug=False)
