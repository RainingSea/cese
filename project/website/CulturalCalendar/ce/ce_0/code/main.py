from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

class UserManager:
    def __init__(self, filename='users.txt'):
        self.filename = filename
    
    def register(self, username, password):
        try:
            with open(self.filename, 'a') as f:
                f.write(f"{username}|{password}\n")
            return True
        except:
            return False
    
    def login(self, username, password):
        try:
            with open(self.filename, 'r') as f:
                for line in f:
                    parts = line.strip().split('|')
                    if len(parts) == 2 and parts[0] == username and parts[1] == password:
                        return True
            return False
        except:
            return False

class EventManager:
    def __init__(self, filename='events.txt'):
        self.filename = filename
    
    def get_events(self):
        events = []
        try:
            with open(self.filename, 'r') as f:
                for line in f:
                    parts = line.strip().split('|')
                    if len(parts) == 6:
                        events.append({
                            'id': parts[0],
                            'name': parts[1],
                            'date': parts[2],
                            'location': parts[3],
                            'description': parts[4],
                            'category': parts[5]
                        })
        except:
            pass
        return events
    
    def search_events(self, query):
        events = self.get_events()
        return [e for e in events if query.lower() in e['name'].lower() or 
                query.lower() in e['description'].lower()]
    
    def get_event_details(self, event_id):
        events = self.get_events()
        for e in events:
            if e['id'] == event_id:
                return e
        return None

class ReminderManager:
    def __init__(self, filename='reminders.txt'):
        self.filename = filename
    
    def add_reminder(self, username, event_id):
        try:
            with open(self.filename, 'a') as f:
                f.write(f"{username}|{event_id}\n")
            return True
        except:
            return False
    
    def get_reminders(self, username):
        reminders = []
        try:
            with open(self.filename, 'r') as f:
                for line in f:
                    parts = line.strip().split('|')
                    if len(parts) == 2 and parts[0] == username:
                        reminders.append(parts[1])
            return reminders
        except:
            return []
    
    def delete_reminder(self, username, event_id):
        try:
            with open(self.filename, 'r') as f:
                lines = f.readlines()
            
            with open(self.filename, 'w') as f:
                for line in lines:
                    parts = line.strip().split('|')
                    if len(parts) == 2 and not (parts[0] == username and parts[1] == event_id):
                        f.write(line)
            return True
        except:
            return False

user_manager = UserManager()
event_manager = EventManager()
reminder_manager = ReminderManager()

@app.route('/')
def home():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.login(username, password):
            session['username'] = username
            return redirect(url_for('dashboard'))
        return render_template('login.html', error='Invalid credentials')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            return redirect(url_for('login'))
        return render_template('register.html', error='Registration failed')
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    query = request.args.get('q', '')
    if query:
        events = event_manager.search_events(query)
    else:
        events = event_manager.get_events()
    
    return render_template('dashboard.html', 
                         username=session['username'],
                         events=events,
                         query=query)

@app.route('/event/<event_id>')
def event_details(event_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    
    event = event_manager.get_event_details(event_id)
    if not event:
        return redirect(url_for('dashboard'))
    
    has_reminder = event_id in reminder_manager.get_reminders(session['username'])
    return render_template('event.html', 
                         event=event,
                         has_reminder=has_reminder)

@app.route('/reminders')
def reminders():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    reminders = reminder_manager.get_reminders(session['username'])
    events = []
    for event_id in reminders:
        event = event_manager.get_event_details(event_id)
        if event:
            events.append(event)
    
    return render_template('reminders.html', events=events)

@app.route('/add_reminder/<event_id>')
def add_reminder(event_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    
    reminder_manager.add_reminder(session['username'], event_id)
    return redirect(url_for('event_details', event_id=event_id))

@app.route('/delete_reminder/<event_id>')
def delete_reminder(event_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    
    reminder_manager.delete_reminder(session['username'], event_id)
    return redirect(url_for('reminders'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8567, debug=False)
