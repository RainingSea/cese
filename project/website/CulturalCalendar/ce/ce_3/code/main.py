from flask import Flask, render_template, request, redirect, session
from user import User
from event import Event
from reminder import Reminder

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def load_users():
    users = []
    with open('users.txt', 'r') as file:
        for line in file:
            username, password = line.strip().split('|')
            users.append(User(username, password))
    return users

def load_events():
    events = []
    with open('events.txt', 'r') as file:
        for line in file:
            title, date, details = line.strip().split('|')
            events.append(Event(title, date, details))
    return events

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
        return redirect('/')
    return render_template('registration.html')

@app.route('/dashboard')
def dashboard():
    events = load_events()
    return render_template('dashboard.html', events=events)

@app.route('/event/<title>')
def event_details(title):
    events = load_events()
    event = next((event for event in events if event.title == title), None)
    return render_template('event_details.html', event=event)

@app.route('/reminders')
def reminders():
    user_reminders = Reminder.load_for_user(session.get('username', ''))
    return render_template('reminders.html', reminders=user_reminders)

if __name__ == '__main__':
    app.run(port=9007, debug=False)
