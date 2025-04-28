from flask import Flask, render_template, request, redirect, session, flash
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class UserManager:
    def __init__(self):
        self.users = self.load_users()

    def load_users(self):
        if not os.path.exists('users.txt'):
            return []
        with open('users.txt', 'r') as file:
            return [line.strip().split('|') for line in file.readlines()]

    def register(self, username: str, password: str) -> bool:
        if any(user[0] == username for user in self.users):
            return False
        self.users.append([username, password])
        with open('users.txt', 'a') as file:
            file.write(f"{username}|{password}\n")
        return True

    def login(self, username: str, password: str) -> bool:
        for user in self.users:
            if user[0] == username and user[1] == password:
                session['username'] = username
                return True
        return False

    def logout(self) -> None:
        session.pop('username', None)

class EntryManager:
    def __init__(self):
        self.entries = self.load_entries()

    def load_entries(self):
        if not os.path.exists('entries.txt'):
            return []
        with open('entries.txt', 'r') as file:
            return [line.strip().split('|') for line in file.readlines()]

    def create_entry(self, username: str, destination: str, dates: str, activities: str, photos: str, reflections: str) -> None:
        entry = [username, destination, dates, activities, photos, reflections]
        self.entries.append(entry)
        with open('entries.txt', 'a') as file:
            file.write('|'.join(entry) + '\n')

    def view_entries(self, username: str) -> list:
        return [entry for entry in self.entries if entry[0] == username]

    def edit_entry(self, entry_id: int, new_data: dict) -> None:
        if 0 <= entry_id < len(self.entries):
            self.entries[entry_id] = [
                new_data.get('username', self.entries[entry_id][0]),
                new_data.get('destination', self.entries[entry_id][1]),
                new_data.get('dates', self.entries[entry_id][2]),
                new_data.get('activities', self.entries[entry_id][3]),
                new_data.get('photos', self.entries[entry_id][4]),
                new_data.get('reflections', self.entries[entry_id][5]),
            ]
            self.save_entries()

    def delete_entry(self, entry_id: int) -> None:
        if 0 <= entry_id < len(self.entries):
            del self.entries[entry_id]
            self.save_entries()

    def search_entries(self, query: str) -> list:
        return [entry for entry in self.entries if query.lower() in entry[1].lower()]

    def save_entries(self) -> None:
        with open('entries.txt', 'w') as file:
            for entry in self.entries:
                file.write('|'.join(entry) + '\n')

user_manager = UserManager()
entry_manager = EntryManager()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.login(username, password):
            return redirect('/dashboard')
        else:
            flash('Invalid credentials, please try again.')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            flash('Registration successful! Please log in.')
            return redirect('/')
        else:
            flash('Username already exists, please choose another.')
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect('/')
    entries = entry_manager.view_entries(session['username'])
    return render_template('dashboard.html', entries=entries)

@app.route('/journal_entry', methods=['GET', 'POST'])
def journal_entry():
    if 'username' not in session:
        return redirect('/')
    if request.method == 'POST':
        destination = request.form['destination']
        dates = request.form['dates']
        activities = request.form['activities']
        photos = request.form['photos']
        reflections = request.form['reflections']
        entry_manager.create_entry(session['username'], destination, dates, activities, photos, reflections)
        flash('Entry created successfully!')
        return redirect('/dashboard')
    return render_template('journal_entry.html')

@app.route('/logout')
def logout():
    user_manager.logout()
    return redirect('/')

if __name__ == '__main__':
    app.run(port=8441, debug=False)
