from flask import Flask, render_template, request, redirect, session, url_for
from flask_session import Session

class UserManager:
    def __init__(self, filename):
        self.filename = filename
        self.load_users()

    def load_users(self):
        self.users = {}
        try:
            with open(self.filename, 'r') as file:
                for line in file:
                    username, password = line.strip().split('|')
                    self.users[username] = password
        except FileNotFoundError:
            open(self.filename, 'w').close()  # Create file if it doesn't exist

    def register(self, username: str, password: str) -> bool:
        if username in self.users:
            return False
        self.users[username] = password
        with open(self.filename, 'a') as file:
            file.write(f"{username}|{password}\n")
        return True

    def login(self, username: str, password: str) -> bool:
        return self.users.get(username) == password

class EventManager:
    def __init__(self, filename):
        self.filename = filename
        self.load_events()

    def load_events(self):
        self.events = {}
        try:
            with open(self.filename, 'r') as file:
                for line in file:
                    event_id, event_name, event_date = line.strip().split('|')
                    self.events[event_id] = {'name': event_name, 'date': event_date}
        except FileNotFoundError:
            open(self.filename, 'w').close()  # Create file if it doesn't exist

    def get_events(self):
        return self.events

    def get_event_details(self, event_id: str):
        return self.events.get(event_id)

class ReminderManager:
    def __init__(self, filename):
        self.filename = filename
        self.load_reminders()

    def load_reminders(self):
        self.reminders = {}
        try:
            with open(self.filename, 'r') as file:
                for line in file:
                    reminder_id, event_id, username = line.strip().split('|')
                    self.reminders[reminder_id] = {'event_id': event_id, 'username': username}
        except FileNotFoundError:
            open(self.filename, 'w').close()  # Create file if it doesn't exist

    def add_reminder(self, event_id: str, username: str) -> bool:
        reminder_id = str(len(self.reminders) + 1)
        self.reminders[reminder_id] = {'event_id': event_id, 'username': username}
        with open(self.filename, 'a') as file:
            file.write(f"{reminder_id}|{event_id}|{username}\n")
        return True

    def get_reminders(self, username: str):
        return {rid: details for rid, details in self.reminders.items() if details['username'] == username}

    def delete_reminder(self, reminder_id: str) -> bool:
        if reminder_id in self.reminders:
            del self.reminders[reminder_id]
            self.save_reminders()
            return True
        return False

    def save_reminders(self):
        with open(self.filename, 'w') as file:
            for rid, details in self.reminders.items():
                file.write(f"{rid}|{details['event_id']}|{details['username']}\n")

app = Flask(__name__)
app.secret_key = 'supersecretkey'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

user_manager = UserManager('users.txt')
event_manager = EventManager('events.txt')
reminder_manager = ReminderManager('reminders.txt')

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    if user_manager.register(username, password):
        return redirect(url_for('login'))
    return "Registration failed", 400

@app.route('/login', methods=['POST'])
def login_post():
    username = request.form['username']
    password = request.form['password']
    if user_manager.login(username, password):
        session['username'] = username
        return redirect(url_for('dashboard'))
    return "Login failed", 400

@app.route('/dashboard')
def dashboard():
    events = event_manager.get_events()
    return render_template('dashboard.html', events=events)

@app.route('/event/<event_id>')
def event_details(event_id):
    event = event_manager.get_event_details(event_id)
    return render_template('event_details.html', event=event, event_id=event_id)

@app.route('/set_reminder', methods=['POST'])
def set_reminder():
    event_id = request.form['event_id']
    username = session.get('username')
    if username:
        reminder_manager.add_reminder(event_id, username)
    return redirect(url_for('reminders'))

@app.route('/reminders')
def reminders():
    username = session.get('username')
    reminders = reminder_manager.get_reminders(username)
    return render_template('reminders.html', reminders=reminders)

@app.route('/delete_reminder/<reminder_id>')
def delete_reminder(reminder_id):
    reminder_manager.delete_reminder(reminder_id)
    return redirect(url_for('reminders'))

if __name__ == '__main__':
    app.run(port=8142, debug=False)
