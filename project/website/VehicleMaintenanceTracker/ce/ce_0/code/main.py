from flask import Flask, render_template, request, redirect, url_for, session
import json
from user import User
from vehicle import Vehicle
from maintenance import Maintenance

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Load users from file
def load_users():
    try:
        with open('users.txt', 'r') as f:
            return [User(*line.strip().split('|')) for line in f.readlines()]
    except FileNotFoundError:
        return []

# Load vehicles from file
def load_vehicles():
    try:
        with open('vehicles.txt', 'r') as f:
            return [Vehicle(*line.strip().split('|')) for line in f.readlines()]
    except FileNotFoundError:
        return []

# Load maintenance records from file
def load_maintenance():
    try:
        with open('maintenance.txt', 'r') as f:
            return [Maintenance(*line.strip().split('|')) for line in f.readlines()]
    except FileNotFoundError:
        return []

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

@app.route('/authenticate', methods=['POST'])
def authenticate():
    username = request.form['username']
    password = request.form['password']
    users = load_users()
    for user in users:
        if user.username == username and user.password == password:
            session['username'] = username
            return redirect(url_for('vehicle_info'))
    return redirect(url_for('login'))

@app.route('/vehicle_info', methods=['GET', 'POST'])
def vehicle_info():
    if request.method == 'POST':
        make = request.form['make']
        model = request.form['model']
        year = request.form['year']
        mileage = request.form['mileage']
        new_vehicle = Vehicle(make, model, year, mileage)
        new_vehicle.save()
        return redirect(url_for('maintenance_tracking'))
    return render_template('vehicle_info.html')

@app.route('/maintenance_tracking')
def maintenance_tracking():
    return render_template('maintenance_tracking.html', maintenance=load_maintenance())

@app.route('/reminders')
def reminders():
    return render_template('reminders.html', maintenance=load_maintenance())

@app.route('/maintenance_history')
def maintenance_history():
    return render_template('maintenance_history.html', maintenance=load_maintenance())

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8683, debug=False)
