from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

class UserManager:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.users = self.load_users()

    def register(self, username: str, password: str) -> bool:
        if username in self.users:
            return False
        with open(self.file_path, 'a') as file:
            file.write(f"{username},{password}\n")
        self.users[username] = password
        return True

    def login(self, username: str, password: str) -> bool:
        return self.users.get(username) == password

    def load_users(self) -> dict:
        users = {}
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r') as file:
                for line in file:
                    username, password = line.strip().split(',')
                    users[username] = password
        return users

class EventManager:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.events = self.load_events()

    def load_events(self) -> list:
        events = []
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r') as file:
                for line in file:
                    events.append(line.strip().split(','))
        return events

    def get_event_details(self, event_name: str) -> str:
        for event in self.events:
            if event[0] == event_name:
                return f"Name: {event[0]}, Significance: {event[1]}, History: {event[2]}, Location: {event[3]}, Date: {event[4]}"
        return "Event not found."

class ReminderManager:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def add_reminder(self, username: str, event_name: str, date: str) -> bool:
        reminder_file = f"reminders_{username}.txt"
        with open(reminder_file, 'a') as file:
            file.write(f"{event_name},{date}\n")
        return True

    def load_reminders(self, username: str) -> list:
        reminders = []
        reminder_file = f"reminders_{username}.txt"
        if os.path.exists(reminder_file):
            with open(reminder_file, 'r') as file:
                for line in file:
                    reminders.append(line.strip().split(','))
        return reminders

user_manager = UserManager('users.txt')
event_manager = EventManager('events.txt')

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    if user_manager.register(username, password):
        return redirect(url_for('login'))
    return "Registration failed. Username may already exist."

@app.route('/dashboard', methods=['POST'])
def dashboard():
    username = request.form['username']
    password = request.form['password']
    if user_manager.login(username, password):
        events = event_manager.events
        return render_template('dashboard.html', events=events, username=username)
    return "Login failed."

@app.route('/event/<event_name>')
def event_details(event_name):
    details = event_manager.get_event_details(event_name)
    return render_template('event_details.html', details=details)

@app.route('/set_reminder', methods=['POST'])
def set_reminder():
    username = request.form['username']
    event_name = request.form['event_name']
    date = request.form['date']
    reminder_manager = ReminderManager(f'reminders_{username}.txt')
    reminder_manager.add_reminder(username, event_name, date)
    return redirect(url_for('dashboard'))

@app.route('/reminders/<username>')
def reminders(username):
    reminder_manager = ReminderManager(f'reminders_{username}.txt')
    reminders = reminder_manager.load_reminders(username)
    return render_template('reminders.html', reminders=reminders)

if __name__ == '__main__':
    app.run(port=8304, debug=False)
