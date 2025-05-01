from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

class UserManager:
    def __init__(self, file_path='users.txt'):
        self.file_path = file_path
        if not os.path.exists(file_path):
            open(file_path, 'w').close()

    def register(self, username, password):
        with open(self.file_path, 'r') as f:
            for line in f:
                if line.startswith(f"{username}|"):
                    return False
        with open(self.file_path, 'a') as f:
            f.write(f"{username}|{password}\n")
        return True

    def login(self, username, password):
        with open(self.file_path, 'r') as f:
            for line in f:
                stored_user, stored_pass = line.strip().split('|')
                if stored_user == username and stored_pass == password:
                    return True
        return False

class EventManager:
    def __init__(self, file_path='events.txt'):
        self.file_path = file_path
        if not os.path.exists(file_path):
            open(file_path, 'w').close()

    def get_events(self):
        events = []
        with open(self.file_path, 'r') as f:
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
        return events

    def get_event(self, event_id):
        with open(self.file_path, 'r') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 6 and parts[0] == event_id:
                    return {
                        'id': parts[0],
                        'name': parts[1],
                        'date': parts[2],
                        'location': parts[3],
                        'description': parts[4],
                        'category': parts[5]
                    }
        return None

    def search_events(self, query):
        if not query:
            return self.get_events()
        query = query.lower()
        events = self.get_events()
        return [e for e in events if query in e['name'].lower() or 
                query in e['description'].lower() or 
                query in e['category'].lower()]

class ReminderManager:
    def __init__(self, file_path='reminders.txt'):
        self.file_path = file_path
        if not os.path.exists(file_path):
            open(file_path, 'w').close()

    def add_reminder(self, user, event_id):
        with open(self.file_path, 'a') as f:
            f.write(f"{user}|{event_id}\n")
        return True

    def get_reminders(self, user):
        reminders = []
        with open(self.file_path, 'r') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 2 and parts[0] == user:
                    reminders.append(parts[1])
        return reminders

    def delete_reminder(self, user, event_id):
        lines = []
        found = False
        with open(self.file_path, 'r') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 2 and parts[0] == user and parts[1] == event_id:
                    found = True
                else:
                    lines.append(line)
        
        if found:
            with open(self.file_path, 'w') as f:
                f.writelines(lines)
            return True
        return False

    def clear_user_reminders(self, user):
        lines = []
        with open(self.file_path, 'r') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 2 and parts[0] != user:
                    lines.append(line)
        
        with open(self.file_path, 'w') as f:
            f.writelines(lines)

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
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.login(username, password):
            session['username'] = username
            return redirect(url_for('dashboard'))
        error = 'Invalid credentials'
    return render_template('login.html', error=error)

@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            return redirect(url_for('login'))
        error = 'Username already exists'
    return render_template('register.html', error=error)

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    query = request.args.get('q', '')
    events = event_manager.search_events(query)
    return render_template('dashboard.html', events=events, username=session['username'])

@app.route('/event/<event_id>')
def event_details(event_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    event = event_manager.get_event(event_id)
    if not event:
        return redirect(url_for('dashboard'))
    has_reminder = event_id in reminder_manager.get_reminders(session['username'])
    return render_template('event.html', event=event, has_reminder=has_reminder)

@app.route('/reminder', methods=['POST'])
def reminder():
    if 'username' not in session:
        return redirect(url_for('login'))
    action = request.form.get('action')
    event_id = request.form.get('event_id')
    
    if action == 'add':
        reminder_manager.add_reminder(session['username'], event_id)
    elif action == 'delete':
        reminder_manager.delete_reminder(session['username'], event_id)
    
    return redirect(url_for('event_details', event_id=event_id))

@app.route('/reminders')
def reminders():
    if 'username' not in session:
        return redirect(url_for('login'))
    reminders = reminder_manager.get_reminders(session['username'])
    events = []
    for event_id in reminders:
        event = event_manager.get_event(event_id)
        if event:
            events.append(event)
    return render_template('reminders.html', events=events)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8569, debug=False)
