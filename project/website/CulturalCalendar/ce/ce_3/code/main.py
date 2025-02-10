from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def save(self) -> bool:
        with open('users.txt', 'a') as f:
            f.write(f"{self.username}|{self.password}\n")
        return True

    def validate_password(self, password: str) -> bool:
        return self.password == password

class Event:
    def __init__(self, event_id: int, title: str, date: str, description: str):
        self.event_id = event_id
        self.title = title
        self.date = date
        self.description = description

    def get_details(self) -> dict:
        return {
            'event_id': self.event_id,
            'title': self.title,
            'date': self.date,
            'description': self.description
        }

class Reminder:
    def __init__(self, user_id: int, event_id: int):
        self.user_id = user_id
        self.event_id = event_id

    def save(self) -> bool:
        with open('reminders.txt', 'a') as f:
            f.write(f"{self.user_id}|{self.event_id}\n")
        return True

def fetch_events() -> list:
    events = []
    if os.path.exists('events.txt'):
        with open('events.txt', 'r') as f:
            for line in f:
                event_id, title, date, description = line.strip().split('|')
                events.append(Event(int(event_id), title, date, description))
    return events

def fetch_event_details(event_id: int) -> dict:
    events = fetch_events()
    for event in events:
        if event.event_id == event_id:
            return event.get_details()
    return {}

def register_user(username: str, password: str) -> bool:
    user = User(username, password)
    return user.save()

def login_user(username: str, password: str) -> bool:
    if os.path.exists('users.txt'):
        with open('users.txt', 'r') as f:
            for line in f:
                stored_username, stored_password = line.strip().split('|')
                if stored_username == username and stored_password == password:
                    return True
    return False

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if login_user(username, password):
            session['username'] = username
            return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        register_user(username, password)
        return redirect(url_for('login'))
    return render_template('registration.html')

@app.route('/dashboard')
def dashboard():
    events = fetch_events()
    return render_template('dashboard.html', events=events)

@app.route('/event/<int:event_id>')
def event_details(event_id):
    event = fetch_event_details(event_id)
    return render_template('event_details.html', event=event)

@app.route('/reminders')
def reminders():
    # Placeholder for reminders implementation
    return render_template('reminders.html')

if __name__ == '__main__':
    app.run(port=8602, debug=False)
