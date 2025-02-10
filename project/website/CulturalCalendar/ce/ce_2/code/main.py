from flask import Flask, render_template, request, redirect, url_for, session
from user import User
from event import Event
from reminder import Reminder
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def load_users():
    users = []
    if os.path.exists('users.txt'):
        with open('users.txt', 'r') as f:
            for line in f:
                username, password = line.strip().split('|')
                users.append(User(username, password))
    return users

def load_events():
    events = []
    if os.path.exists('events.txt'):
        with open('events.txt', 'r') as f:
            for line in f:
                title, date, details = line.strip().split('|')
                events.append(Event(title, date, details))
    return events

def load_reminders():
    reminders = []
    if os.path.exists('reminders.txt'):
        with open('reminders.txt', 'r') as f:
            for line in f:
                user, event_title = line.strip().split('|')
                reminders.append(Reminder(user, event_title))
    return reminders

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User(username, password)
        user.save()
        return redirect(url_for('login'))
    return render_template('registration.html')

@app.route('/dashboard', methods=['GET'])
def dashboard():
    events = load_events()
    return render_template('dashboard.html', events=events)

@app.route('/event/<title>', methods=['GET'])
def event_details(title):
    events = load_events()
    event = next((event for event in events if event.title == title), None)
    return render_template('event_details.html', event=event)

@app.route('/reminders', methods=['GET'])
def reminders():
    user = session.get('username')
    reminders = load_reminders()
    user_reminders = [reminder for reminder in reminders if reminder.user == user]
    return render_template('reminders.html', reminders=user_reminders)

if __name__ == '__main__':
    app.run(port=8601, debug=False)
