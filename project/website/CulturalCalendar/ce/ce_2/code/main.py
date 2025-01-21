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
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    events = event_manager.load_events()
    return render_template('dashboard.html', events=events)

@app.route('/event/<int:event_id>')
def event_details(event_id):
    event = event_manager.get_event_details(event_id)
    return render_template('event_details.html', event=event)

@app.route('/reminders')
def reminders():
    user = session.get('username')
    reminders = reminder_manager.load_reminders(user) if user else []
    return render_template('reminders.html', reminders=reminders)

if __name__ == '__main__':
    app.run(port=9006, debug=False)
