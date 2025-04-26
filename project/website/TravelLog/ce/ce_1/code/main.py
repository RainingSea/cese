from flask import Flask, render_template, request, redirect, url_for, session
import json
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class UserManager:
    def __init__(self):
        self.users = self.load_users()

    def load_users(self):
        if not os.path.exists('users.txt'):
            return {}
        with open('users.txt', 'r') as file:
            users = {}
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
        return self.users.get(username) == password

class EntryManager:
    def __init__(self):
        self.entries = self.load_entries()

    def load_entries(self):
        if not os.path.exists('entries.txt'):
            return []
        with open('entries.txt', 'r') as file:
            entries = []
            for line in file:
                entries.append(json.loads(line.strip()))
            return entries

    def create_entry(self, destination: str, date: str, activities: str, photos: list, reflections: str) -> bool:
        entry = {
            'destination': destination,
            'date': date,
            'activities': activities,
            'photos': photos,
            'reflections': reflections
        }
        self.entries.append(entry)
        with open('entries.txt', 'a') as file:
            file.write(json.dumps(entry) + '\n')
        return True

    def view_entries(self) -> list:
        return self.entries

    def edit_entry(self, entry_id: int, updated_data: dict) -> bool:
        if 0 <= entry_id < len(self.entries):
            self.entries[entry_id].update(updated_data)
            self.save_entries()
            return True
        return False

    def delete_entry(self, entry_id: int) -> bool:
        if 0 <= entry_id < len(self.entries):
            del self.entries[entry_id]
            self.save_entries()
            return True
        return False

    def save_entries(self):
        with open('entries.txt', 'w') as file:
            for entry in self.entries:
                file.write(json.dumps(entry) + '\n')

    def search_entries(self, query: str) -> list:
        return [entry for entry in self.entries if query.lower() in entry['destination'].lower()]

class Main:
    def __init__(self):
        self.user_manager = UserManager()
        self.entry_manager = EntryManager()

    def main(self):
        app.run(port=8267, debug=False)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if app.user_manager.register(username, password):
            return redirect(url_for('login'))
        return "Registration failed. Username may already exist."
    return render_template('registration.html')

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if app.user_manager.login(username, password):
            session['username'] = username
            return redirect(url_for('journal_entry'))
        return "Login failed. Please check your credentials."
    return render_template('login.html')

@app.route('/journal_entry', methods=['GET', 'POST'])
def journal_entry():
    if request.method == 'POST':
        destination = request.form['destination']
        date = request.form['date']
        activities = request.form['activities']
        photos = request.files.getlist('photos')
        reflections = request.form['reflections']
        photo_filenames = [photo.filename for photo in photos]
        app.entry_manager.create_entry(destination, date, activities, photo_filenames, reflections)
        return redirect(url_for('journal_entry'))
    entries = app.entry_manager.view_entries()
    return render_template('journal_entry.html', entries=entries)

@app.route('/search', methods=['GET', 'POST'])
def search():
    results = []
    if request.method == 'POST':
        query = request.form['query']
        results = app.entry_manager.search_entries(query)
    return render_template('search.html', results=results)

@app.route('/share', methods=['GET'])
def share():
    return render_template('share.html')

if __name__ == '__main__':
    app_instance = Main()
    app_instance.main()