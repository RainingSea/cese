from flask import Flask, render_template, request, redirect, url_for, flash, session
from user import User
from event import Event
from reminder import Reminder
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Load data from files
def load_users():
    return User.load_all()

def load_events():
    return Event.load_all()

def load_reminders():
    return Reminder.load_for_user(session.get('username', None))

users = load_users()
events = load_events()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        for user in users:
            if user.validate(username, password):
                session['username'] = username
                return redirect(url_for('dashboard'))
        flash('Invalid username or password')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if any(user.username == username for user in users):
            flash('Username already exists')
        else:
            new_user = User(username, password)
            new_user.save()
            users.append(new_user)
            flash('Registration successful! Please log in.')
            return redirect(url_for('login'))
    return render_template('registration.html')

@app.route('/dashboard')
def dashboard():
    reminders = load_reminders()
    if not events:
        flash('No upcoming events found.')
    return render_template('dashboard.html', events=events, reminders=reminders)

@app.route('/event/<title>')
def event_details(title):
    event = next((event for event in events if event.title == title), None)
    if event is None:
        flash('Event not found.')
        return redirect(url_for('dashboard'))
    return render_template('event_details.html', event=event)

@app.route('/reminders', methods=['GET', 'POST'])
def reminders_page():
    if request.method == 'POST':
        user = session.get('username')
        event_title = request.form['event_title']
        reminder_date = request.form['reminder_date']
        new_reminder = Reminder(user, event_title, reminder_date)
        new_reminder.save()
        flash('Reminder set successfully!')
    reminders = load_reminders()
    return render_template('reminders.html', reminders=reminders)

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out.')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=9009, debug=False)
