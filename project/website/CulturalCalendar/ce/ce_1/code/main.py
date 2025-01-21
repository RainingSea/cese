from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from data_manager import DataManager
from models import User, Event, Reminder

app = Flask(__name__)
app.secret_key = 'your_secret_key'
data_manager = DataManager()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User(username, generate_password_hash(password))
        data_manager.save_user(user)
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    events = data_manager.load_events()
    return render_template('dashboard.html', events=events)

@app.route('/event/<title>')
def event_details(title):
    events = data_manager.load_events()
    event = next((event for event in events if event.title == title), None)
    return render_template('event_details.html', event=event)

@app.route('/set_reminder', methods=['POST'])
def set_reminder():
    user = session.get('username')
    event_title = request.form['event_title']
    reminder = Reminder(user, event_title)
    data_manager.save_reminder(reminder)
    return redirect(url_for('reminders'))

@app.route('/reminders')
def reminders():
    user = session.get('username')
    reminders = data_manager.load_reminders()
    user_reminders = [reminder for reminder in reminders if reminder.user == user]
    return render_template('reminders.html', reminders=user_reminders)

if __name__ == '__main__':
    app.run(port=9005, debug=False)
