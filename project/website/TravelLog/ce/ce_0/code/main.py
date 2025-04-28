from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class UserManager:
    def __init__(self):
        self.users = self.load_users()

    def load_users(self):
        users = {}
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
            session['username'] = username
            return True
        return False

    def logout(self) -> None:
        session.pop('username', None)

class EntryManager:
    def __init__(self):
        self.entries = self.load_entries()

    def load_entries(self):
        entries = []
        with open('entries.txt', 'r') as file:
            for line in file:
                entries.append(line.strip().split(','))
        return entries

    def create_entry(self, destination: str, date: str, activities: str, photos: str, reflections: str) -> None:
        entry = [destination, date, activities, photos, reflections]
        self.entries.append(entry)
        with open('entries.txt', 'a') as file:
            file.write(','.join(entry) + '\n')

    def edit_entry(self, entry_id: int, new_data: str) -> None:
        if 0 <= entry_id < len(self.entries):
            self.entries[entry_id] = new_data.split(',')
            self.save_entries()

    def delete_entry(self, entry_id: int) -> None:
        if 0 <= entry_id < len(self.entries):
            del self.entries[entry_id]
            self.save_entries()

    def search_entries(self, query: str) -> list:
        return [entry for entry in self.entries if query in entry]

    def get_entries(self) -> list:
        return self.entries

    def save_entries(self) -> None:
        with open('entries.txt', 'w') as file:
            for entry in self.entries:
                file.write(','.join(entry) + '\n')

user_manager = UserManager()
entry_manager = EntryManager()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.login(username, password):
            return redirect(url_for('overview'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/overview')
def overview():
    entries = entry_manager.get_entries()
    return render_template('overview.html', entries=entries)

@app.route('/journal', methods=['GET', 'POST'])
def journal():
    if request.method == 'POST':
        destination = request.form['destination']
        date = request.form['date']
        activities = request.form['activities']
        photos = request.files['photos']
        reflections = request.form['reflections']
        if photos:
            filename = secure_filename(photos.filename)
            photos.save(os.path.join('uploads', filename))
            entry_manager.create_entry(destination, date, activities, filename, reflections)
            return redirect(url_for('overview'))
    return render_template('journal.html')

@app.route('/logout')
def logout():
    user_manager.logout()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8438, debug=False)
