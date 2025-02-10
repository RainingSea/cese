from flask import Flask, render_template, request, redirect, url_for, session
from bcrypt import hashpw, gensalt, checkpw
from user import User
from event import Event
from reminder import Reminder

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def load_users():
    users = []
    try:
        with open('users.txt', 'r') as file:
            for line in file:
                username, password = line.strip().split('|')
                users.append(User(username, password))
    except FileNotFoundError:
        pass
    return users

def load_events():
    events = []
    try:
        with open('events.txt', 'r') as file:
            for line in file:
                name, significance, history, location = line.strip().split('|')
                events.append(Event(name, significance, history, location))
    except FileNotFoundError:
        pass
    return events

def load_reminders():
    reminders = []
    try:
        with open('reminders.txt', 'r') as file:
            for line in file:
                username, event_name = line.strip().split('|')
                reminders.append(Reminder(username, event_name))
    except FileNotFoundError:
        pass
    return reminders

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = hashpw(password.encode('utf-8'), gensalt())
        user = User(username, hashed_password.decode('utf-8'))
        user.save()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    events = load_events()
    return render_template('dashboard.html', events=events)

@app.route('/event/<event_name>')
def event_details(event_name):
    events = load_events()
    event = next((e for e in events if e.name == event_name), None)
    return render_template('event_details.html', event=event)

@app.route('/reminders')
def reminders():
    username = session.get('username')
    reminders = load_reminders()
    user_reminders = [r for r in reminders if r.username == username]
    return render_template('reminders.html', reminders=user_reminders)

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    users = load_users()
    user = next((u for u in users if u.username == username), None)
    if user and checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        session['username'] = username
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/set_reminder', methods=['POST'])
def set_reminder():
    username = session.get('username')
    event_name = request.form['event_name']
    reminder = Reminder(username, event_name)
    reminder.save()
    return redirect(url_for('reminders'))

if __name__ == '__main__':
    app.run(port=8600, debug=False)
