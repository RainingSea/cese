from flask import Flask, render_template, request, redirect, session, flash
from datetime import datetime
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
        for user in self.users:
            if user[0] == username:
                return False
        self.users.append([username, password])
        self.save_users()
        return True

    def save_users(self):
        with open('users.txt', 'w') as file:
            for user in self.users:
                file.write('|'.join(user) + '\n')

    def login(self, username: str, password: str) -> bool:
        for user in self.users:
            if user[0] == username and user[1] == password:
                return True
        return False

    def logout(self):
        session.pop('username', None)

class EventManager:
    def __init__(self):
        self.events = self.load_events()

    def load_events(self):
        if not os.path.exists('events.txt'):
            return []
        with open('events.txt', 'r') as file:
            return [line.strip().split('|') for line in file.readlines()]

    def get_events(self):
        return self.events

    def get_event_details(self, event_id: int) -> str:
        return self.events[event_id] if 0 <= event_id < len(self.events) else None

    def search_events(self, query: str):
        return [event for event in self.events if query.lower() in event[1].lower()]

class ReminderManager:
    def __init__(self):
        self.reminders = self.load_reminders()

    def load_reminders(self):
        if not os.path.exists('reminders.txt'):
            return []
        with open('reminders.txt', 'r') as file:
            return [line.strip().split('|') for line in file.readlines()]

    def add_reminder(self, event_id: int) -> bool:
        self.reminders.append([str(event_id), datetime.now().isoformat()])
        self.save_reminders()
        return True

    def remove_reminder(self, reminder_id: int) -> bool:
        if 0 <= reminder_id < len(self.reminders):
            del self.reminders[reminder_id]
            self.save_reminders()
            return True
        return False

    def save_reminders(self):
        with open('reminders.txt', 'w') as file:
            for reminder in self.reminders:
                file.write('|'.join(reminder) + '\n')

    def get_reminders(self):
        return self.reminders

user_manager = UserManager()
event_manager = EventManager()
reminder_manager = ReminderManager()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.login(username, password):
            session['username'] = username
            return redirect('/dashboard')
        flash("Invalid credentials", "error")
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            return redirect('/')
        flash("Username already in use", "error")
    return render_template('registration.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect('/')
    events = event_manager.get_events()
    return render_template('dashboard.html', events=events)

@app.route('/event/<int:event_id>', methods=['GET', 'POST'])
def event_details(event_id):
    event = event_manager.get_event_details(event_id)
    if request.method == 'POST':
        if reminder_manager.add_reminder(event_id):
            return redirect('/reminders')
    return render_template('event_details.html', event=event)

@app.route('/reminders', methods=['GET', 'POST'])
def reminders():
    if 'username' not in session:
        return redirect('/')
    if request.method == 'POST':
        reminder_id = int(request.form['reminder_id'])
        reminder_manager.remove_reminder(reminder_id)
        return redirect('/reminders')
    reminders = reminder_manager.get_reminders()
    return render_template('reminders.html', reminders=reminders)

@app.route('/logout')
def logout():
    user_manager.logout()
    return redirect('/')

if __name__ == '__main__':
    app.run(port=8306, debug=False)
