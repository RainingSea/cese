from flask import Flask, render_template, request, redirect, session, url_for
from flask_session import Session
from user_manager import UserManager
from event_manager import EventManager
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

user_manager = UserManager()
event_manager = EventManager()

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
    return render_template('registration.html')

@app.route('/dashboard')
def dashboard():
    events = event_manager.load_events()
    return render_template('dashboard.html', events=events)

@app.route('/event/<event_title>')
def event_details(event_title):
    event_info = event_manager.get_event_details(event_title)
    return render_template('event_details.html', event=event_info)

@app.route('/reminders')
def reminders():
    username = session.get('username')
    user_reminders = event_manager.get_reminders(username)
    return render_template('reminders.html', reminders=user_reminders)

@app.route('/set_reminder/<event_title>')
def set_reminder(event_title):
    username = session.get('username')
    event_manager.set_reminder(username, event_title)
    return redirect(url_for('reminders'))

if __name__ == '__main__':
    app.run(port=8141, debug=False)
