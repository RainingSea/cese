from flask import Flask, render_template, request, redirect, session, flash
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class UserManager:
    def __init__(self, users_file: str):
        self.users_file = users_file
        self.load_users()

    def load_users(self) -> None:
        """Load users from the specified file."""
        self.users = {}
        if os.path.exists(self.users_file):
            with open(self.users_file, 'r') as file:
                for line in file:
                    username, password = line.strip().split(',')
                    self.users[username] = password

    def register(self, username: str, password: str) -> bool:
        """Register a new user if the username does not already exist."""
        if username in self.users:
            return False
        with open(self.users_file, 'a') as file:
            file.write(f"{username},{password}\n")
        self.users[username] = password
        return True

    def login(self, username: str, password: str) -> bool:
        """Check if the username and password match."""
        return self.users.get(username) == password

    def get_users(self) -> list:
        """Return a list of registered usernames."""
        return list(self.users.keys())

class JournalManager:
    def __init__(self, entries_file: str):
        self.entries_file = entries_file
        self.load_entries()

    def load_entries(self) -> None:
        """Load journal entries from the specified file."""
        self.entries = []
        if os.path.exists(self.entries_file):
            with open(self.entries_file, 'r') as file:
                for line in file:
                    title, date, content = line.strip().split('|')
                    self.entries.append({'title': title, 'date': date, 'content': content})

    def create_entry(self, title: str, content: str) -> bool:
        """Create a new journal entry."""
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.entries_file, 'a') as file:
            file.write(f"{title}|{date}|{content}\n")
        self.entries.append({'title': title, 'date': date, 'content': content})
        return True

    def get_entries(self) -> list:
        """Return a list of journal entries."""
        return self.entries

    def delete_entry(self, title: str) -> bool:
        """Delete a journal entry by title."""
        self.entries = [entry for entry in self.entries if entry['title'] != title]
        self.save_entries()
        return True

    def update_entry(self, title: str, new_content: str) -> bool:
        """Update the content of an existing journal entry."""
        for entry in self.entries:
            if entry['title'] == title:
                entry['content'] = new_content
                self.save_entries()
                return True
        return False

    def save_entries(self) -> None:
        """Save all journal entries back to the file."""
        with open(self.entries_file, 'w') as file:
            for entry in self.entries:
                file.write(f"{entry['title']}|{entry['date']}|{entry['content']}\n")

user_manager = UserManager('users.txt')
journal_manager = JournalManager('entries.txt')

@app.route('/', methods=['GET', 'POST'])
def login():
    """Handle user login."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.login(username, password):
            session['username'] = username
            return redirect('/dashboard')
        else:
            flash('Invalid username or password')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Handle user registration."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            flash('Registration successful! Please log in.')
            return redirect('/')
        else:
            flash('Username already exists.')
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    """Display the user dashboard with journal entries."""
    if 'username' not in session:
        return redirect('/')
    entries = journal_manager.get_entries()
    return render_template('dashboard.html', entries=entries)

@app.route('/new_entry', methods=['GET', 'POST'])
def new_entry():
    """Create a new journal entry."""
    if 'username' not in session:
        return redirect('/')
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        journal_manager.create_entry(title, content)
        return redirect('/dashboard')
    return render_template('new_entry.html')

@app.route('/logout')
def logout():
    """Log out the user."""
    session.pop('username', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(port=8158, debug=False)
