from flask import Flask, render_template, request, redirect, url_for, session
from user_manager import UserManager
from event_manager import EventManager
from reminder_manager import ReminderManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'

user_manager = UserManager('users.txt')
event_manager = EventManager('events.txt')
reminder_manager = ReminderManager('reminders.txt')

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
    events = event_manager.load_events()
    return render_template('dashboard.html', events=events)

@app.route('/event/<int:event_id>', methods=['GET'])
def event_details(event_id):
    event = event_manager.get_event_details(event_id)
    return render_template('event_details.html', event=event)

@app.route('/reminders', methods=['GET'])
def reminders():
    username = session.get('username')
    reminders = reminder_manager.load_reminders(username)
    return render_template('reminders.html', reminders=reminders)

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    if user_manager.login(username, password):
        session['username'] = username
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=9008, debug=False)
