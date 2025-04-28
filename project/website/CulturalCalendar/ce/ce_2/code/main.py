from flask import Flask, render_template, request, redirect, url_for, session
from UserManager import UserManager
from EventManager import EventManager
from ReminderManager import ReminderManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'

user_manager = UserManager()
event_manager = EventManager()
reminder_manager = ReminderManager()

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

@app.route('/dashboard', methods=['GET'])
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    events = event_manager.load_events()
    return render_template('dashboard.html', events=events)

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    if user_manager.login(username, password):
        session['username'] = username
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/event/<int:event_id>', methods=['GET'])
def event_details(event_id):
    event = event_manager.events[event_id]
    return render_template('event_details.html', event=event)

@app.route('/set_reminder/<int:event_id>', methods=['POST'])
def set_reminder(event_id):
    username = session['username']
    reminder_manager.set_reminder(username, event_id)
    return redirect(url_for('dashboard'))

@app.route('/reminders', methods=['GET'])
def reminders():
    username = session['username']
    reminders = reminder_manager.get_reminders(username)
    return render_template('reminders.html', reminders=reminders)

if __name__ == '__main__':
    app.run(port=8305, debug=False)
