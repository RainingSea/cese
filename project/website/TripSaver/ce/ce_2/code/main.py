from flask import Flask, render_template, request, redirect, url_for, session
from auth import AuthManager
from trip_manager import TripManager

app = Flask(__name__)
app.secret_key = 'secret_key'

auth_manager = AuthManager('users.txt')
trip_manager = TripManager('trips.txt', 'transport_data.txt')

@app.route('/')
def home():
    if 'username' in session:
        return redirect(url_for('trip_planner'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if auth_manager.login(username, password):
            session['username'] = username
            return redirect(url_for('trip_planner'))
        return "Invalid credentials", 401
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if auth_manager.register(username, password):
            return redirect(url_for('login'))
        return "Username already exists", 400
    return render_template('register.html')

@app.route('/trip', methods=['GET'])
def trip_planner():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('trip.html')

@app.route('/plan_trip', methods=['POST'])
def plan_trip():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    origin = request.form['origin']
    destination = request.form['destination']
    date = request.form['date']
    
    options = trip_manager.get_transport_options(origin, destination)
    comparison = trip_manager.compare_options(options)
    
    return render_template('trip.html', options=comparison)

@app.route('/save_trip', methods=['GET'])
def save_trip():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    origin = request.args.get('origin')
    destination = request.args.get('destination')
    date = request.args.get('date')
    
    if origin and destination and date:
        trip_manager.save_trip(session['username'], origin, destination, date)
        return "Trip saved successfully", 200
    return "Missing trip details", 400

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8077, debug=False)
