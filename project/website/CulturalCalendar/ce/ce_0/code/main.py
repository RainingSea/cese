from flask import Flask, render_template, request, redirect, url_for, session
from data_manager import DataManager, User, Event, Reminder

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        new_user = User(username, password)
        new_user.save()
        return redirect(url_for('login'))
    return render_template('registration.html')

@app.route('/dashboard')
def dashboard():
    events = DataManager.load_events()
    return render_template('dashboard.html', events=events)

@app.route('/event/<title>')
def event_details(title):
    events = DataManager.load_events()
    event = next((event for event in events if event.title == title), None)
    return render_template('event_details.html', event=event)

@app.route('/reminders')
def reminders():
    user_reminders = DataManager.load_reminders()
    return render_template('reminders.html', reminders=user_reminders)

if __name__ == '__main__':
    app.run(port=9004, debug=False)
