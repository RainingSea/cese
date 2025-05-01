from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime
import json
import os

app = Flask(__name__)
app.secret_key = 'secret_key'

class UserManager:
    def __init__(self, users_file='users.txt'):
        self.users_file = users_file
        if not os.path.exists(users_file):
            open(users_file, 'w').close()

    def register(self, username, password):
        with open(self.users_file, 'r') as f:
            for line in f:
                if line.startswith(f"{username}|"):
                    return False
        with open(self.users_file, 'a') as f:
            f.write(f"{username}|{password}\n")
        return True

    def login(self, username, password):
        with open(self.users_file, 'r') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 2 and parts[0] == username and parts[1] == password:
                    return True
        return False

class EventManager:
    def __init__(self, events_file='events.txt'):
        self.events_file = events_file
        if not os.path.exists(events_file):
            open(events_file, 'w').close()

    def get_events(self):
        events = []
        with open(self.events_file, 'r') as f:
            for line in f:
                try:
                    events.append(json.loads(line.strip()))
                except json.JSONDecodeError:
                    continue
        return events

    def search_events(self, query):
        events = self.get_events()
        return [e for e in events if query.lower() in e['title'].lower() or 
                query.lower() in e['description'].lower()]

    def get_event(self, event_id):
        with open(self.events_file, 'r') as f:
            for line in f:
                try:
                    event = json.loads(line.strip())
                    if str(event['id']) == str(event_id):
                        return event
                except json.JSONDecodeError:
                    continue
        return None

class ReminderManager:
    def __init__(self, reminders_file='reminders.txt'):
        self.reminders_file = reminders_file
        if not os.path.exists(reminders_file):
            open(reminders_file, 'w').close()

    def add_reminder(self, user, event_id):
        with open(self.reminders_file, 'a') as f:
            f.write(f"{user}|{event_id}\n")
        return True

    def get_reminders(self, user):
        reminders = []
        with open(self.reminders_file, 'r') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 2 and parts[0] == user:
                    reminders.append(parts[1])
        return reminders

    def delete_reminder(self, user, event_id):
        lines = []
        with open(self.reminders_file, 'r') as f:
            lines = f.readlines()
        
        with open(self.reminders_file, 'w') as f:
            for line in lines:
                parts = line.strip().split('|')
                if not (len(parts) == 2 and parts[0] == user and parts[1] == event_id):
                    f.write(line)
        return True

user_manager = UserManager()
event_manager = EventManager()
reminder_manager = ReminderManager()

@app.route('/')
def home():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.login(username, password):
            session['username'] = username
            return redirect(url_for('dashboard'))
        return render_template('login.html', error='Invalid credentials')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            return redirect(url_for('login'))
        return render_template('register.html', error='Username already exists')
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    events = event_manager.get_events()
    return render_template('dashboard.html', username=session['username'], events=events)

@app.route('/search')
def search():
    if 'username' not in session:
        return redirect(url_for('login'))
    query = request.args.get('q', '')
    events = event_manager.search_events(query)
    return render_template('dashboard.html', username=session['username'], events=events, search_query=query)

@app.route('/event/<event_id>')
def event(event_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    event = event_manager.get_event(event_id)
    if not event:
        return redirect(url_for('dashboard'))
    return render_template('event.html', event=event, username=session['username'])

@app.route('/reminders')
def reminders():
    if 'username' not in session:
        return redirect(url_for('login'))
    reminder_ids = reminder_manager.get_reminders(session['username'])
    events = [event_manager.get_event(id) for id in reminder_ids]
    events = [e for e in events if e is not None]
    return render_template('reminders.html', username=session['username'], events=events)

@app.route('/add_reminder/<event_id>')
def add_reminder(event_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    reminder_manager.add_reminder(session['username'], event_id)
    return redirect(url_for('reminders'))

@app.route('/delete_reminder/<event_id>')
def delete_reminder(event_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    reminder_manager.delete_reminder(session['username'], event_id)
    return redirect(url_for('reminders'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8568, debug=False)
