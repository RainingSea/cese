from flask import Flask, render_template, request, redirect, url_for, session
from user_manager import UserManager
from event_manager import EventManager
from reminder_manager import ReminderManager

app = Flask(__name__)
app.secret_key = 'supersecretkey'

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

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', events=event_manager.events)

@app.route('/event/<int:event_id>')
def event_details(event_id):
    event = event_manager.get_event_details(event_id)
    return render_template('event_details.html', event=event)

@app.route('/reminders')
def reminders():
    user_id = session.get('user_id')
    user_reminders = reminder_manager.reminders.get(user_id, [])
    return render_template('reminders.html', reminders=user_reminders)

@app.route('/authenticate', methods=['POST'])
def authenticate():
    username = request.form['username']
    password = request.form['password']
    if user_manager.login(username, password):
        session['user_id'] = username
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8599, debug=False)
