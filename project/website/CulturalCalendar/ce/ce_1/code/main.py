from flask import Flask, render_template, request, redirect, url_for, session
from flask_httpauth import HTTPBasicAuth
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'
auth = HTTPBasicAuth()

class UserManager:
    def __init__(self):
        self.users = self.load_users()

    def load_users(self):
        users = {}
        if os.path.exists('users.txt'):
            with open('users.txt', 'r') as file:
                for line in file:
                    username, password = line.strip().split(',')
                    users[username] = password
        return users

    def register(self, username: str, password: str) -> bool:
        if username in self.users:
            return False
        self.users[username] = password
        with open('users.txt', 'a') as file:
            file.write(f"{username},{password}\n")
        return True

    def login(self, username: str, password: str) -> bool:
        return self.users.get(username) == password

class EventManager:
    def __init__(self):
        self.events = self.load_events()

    def load_events(self):
        events = []
        if os.path.exists('events.txt'):
            with open('events.txt', 'r') as file:
                for line in file:
                    event_name, significance, history, location, date = line.strip().split(',')
                    events.append({
                        'event_name': event_name,
                        'significance': significance,
                        'history': history,
                        'location': location,
                        'date': date
                    })
        return events

    def get_event_details(self, event_name: str):
        for event in self.events:
            if event['event_name'] == event_name:
                return event
        return None

class ReminderManager:
    def __init__(self):
        self.reminders = self.load_reminders()

    def load_reminders(self):
        reminders = {}
        if os.path.exists('reminders.txt'):
            with open('reminders.txt', 'r') as file:
                for line in file:
                    username, event_name = line.strip().split(',')
                    if username not in reminders:
                        reminders[username] = []
                    reminders[username].append(event_name)
        return reminders

    def set_reminder(self, username: str, event_name: str) -> bool:
        if username not in self.reminders:
            self.reminders[username] = []
        if event_name in self.reminders[username]:
            return False
        self.reminders[username].append(event_name)
        with open('reminders.txt', 'a') as file:
            file.write(f"{username},{event_name}\n")
        return True

    def get_reminders(self, username: str):
        return self.reminders.get(username, [])

user_manager = UserManager()
event_manager = EventManager()
reminder_manager = ReminderManager()

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
        return 'User already exists!'
    return render_template('registration.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', events=event_manager.events)

@app.route('/event/<event_name>')
def event_details(event_name):
    event = event_manager.get_event_details(event_name)
    return render_template('event_details.html', event=event)

@app.route('/set_reminder/<event_name>', methods=['POST'])
def set_reminder(event_name):
    username = session.get('username')
    if username:
        reminder_manager.set_reminder(username, event_name)
    return redirect(url_for('dashboard'))

@app.route('/reminders')
def reminders():
    username = session.get('username')
    user_reminders = reminder_manager.get_reminders(username)
    return render_template('reminders.html', reminders=user_reminders)

@auth.login_required
@app.route('/login', methods=['GET', 'POST'])
def do_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.login(username, password):
            session['username'] = username
            return redirect(url_for('dashboard'))
        return 'Invalid credentials!'
    return render_template('login.html')

if __name__ == '__main__':
    app.run(port=8140, debug=False)
