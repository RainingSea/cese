from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

class UserManager:
    def __init__(self, users_file='users.txt'):
        self.users_file = users_file
    
    def register(self, username, password):
        with open(self.users_file, 'a+') as f:
            f.seek(0)
            for line in f:
                if line.startswith(f"{username}|"):
                    return False
            f.write(f"{username}|{password}\n")
        return True
    
    def login(self, username, password):
        with open(self.users_file, 'r') as f:
            for line in f:
                stored_username, stored_password = line.strip().split('|')
                if stored_username == username and stored_password == password:
                    return True
        return False

class TripManager:
    def __init__(self, trips_file='trips.txt'):
        self.trips_file = trips_file
    
    def save_trip(self, username, start, destination, date):
        with open(self.trips_file, 'a') as f:
            f.write(f"{username}|{start}|{destination}|{date}\n")
        return True
    
    def get_transport_options(self, start, destination):
        # Mock data for demonstration
        return [
            {"mode": "Car", "cost": 50, "time": "2 hours"},
            {"mode": "Train", "cost": 30, "time": "3 hours"},
            {"mode": "Bus", "cost": 20, "time": "4 hours"},
            {"mode": "Plane", "cost": 150, "time": "1 hour"}
        ]

class PreferenceManager:
    def __init__(self, preferences_file='preferences.txt'):
        self.preferences_file = preferences_file
    
    def save_preference(self, username, transport_mode, start, destination):
        with open(self.preferences_file, 'a') as f:
            f.write(f"{username}|{transport_mode}|{start}|{destination}\n")
        return True
    
    def get_preferences(self, username):
        preferences = []
        with open(self.preferences_file, 'r') as f:
            for line in f:
                parts = line.strip().split('|')
                if parts[0] == username:
                    preferences.append({
                        "transport_mode": parts[1],
                        "start": parts[2],
                        "destination": parts[3]
                    })
        return preferences

user_manager = UserManager()
trip_manager = TripManager()
preference_manager = PreferenceManager()

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.login(username, password):
            session['username'] = username
            return redirect(url_for('trip_input'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        if password == confirm_password and user_manager.register(username, password):
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/trip_input', methods=['GET', 'POST'])
def trip_input():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        start = request.form['start']
        destination = request.form['destination']
        date = request.form['date']
        trip_manager.save_trip(session['username'], start, destination, date)
        transport_options = trip_manager.get_transport_options(start, destination)
        return render_template('results.html', options=transport_options, start=start, destination=destination)
    return render_template('trip_input.html')

@app.route('/save_preference', methods=['POST'])
def save_preference():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    transport_mode = request.form['transport_mode']
    start = request.form['start']
    destination = request.form['destination']
    preference_manager.save_preference(session['username'], transport_mode, start, destination)
    return redirect(url_for('preferences'))

@app.route('/preferences')
def preferences():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    user_preferences = preference_manager.get_preferences(session['username'])
    return render_template('preferences.html', preferences=user_preferences)

@app.route('/compare', methods=['POST'])
def compare():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    option1 = request.form.get('option1')
    option2 = request.form.get('option2')
    start = request.form.get('start')
    destination = request.form.get('destination')
    
    if not option1 or not option2:
        return redirect(url_for('trip_input'))
    
    transport_options = trip_manager.get_transport_options(start, destination)
    option1_data = next((opt for opt in transport_options if opt['mode'] == option1), None)
    option2_data = next((opt for opt in transport_options if opt['mode'] == option2), None)
    
    return render_template('compare.html', option1=option1_data, option2=option2_data)

if __name__ == '__main__':
    app.run(port=8076, debug=False)
