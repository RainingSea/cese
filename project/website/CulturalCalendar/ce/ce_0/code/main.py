from flask import Flask, render_template, request, redirect, url_for, session
from user_manager import UserManager
from event_manager import EventManager
from reminder import Reminder

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a random secret key
user_manager = UserManager()
event_manager = EventManager()
reminder_manager = Reminder()

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
    if 'username' in session:
        events = event_manager.get_events()
        return render_template('dashboard.html', events=events)
    return redirect(url_for('login'))

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    if user_manager.login(username, password):
        session['username'] = username
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/event/<event_id>')
def event_details(event_id):
    event_details = event_manager.get_event_details(event_id)
    return render_template('event_details.html', event=event_details)

@app.route('/reminders')
def reminders():
    if 'username' in session:
        user_reminders = reminder_manager.get_reminders(session['username'])
        return render_template('reminders.html', reminders=user_reminders)
    return redirect(url_for('login'))

@app.route('/set_reminder/<event_id>', methods=['POST'])
def set_reminder(event_id):
    if 'username' in session:
        reminder_manager.add_reminder(session['username'], event_id)
    return redirect(url_for('reminders'))

if __name__ == '__main__':
    app.run(port=8303, debug=False)
