from flask import Flask, render_template, request, redirect, url_for, session
import json
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def save_to_file(self):
        with open('users.txt', 'a') as f:
            f.write(f"{self.username}|{self.password}\n")

class Vehicle:
    def __init__(self, make: str, model: str, year: int, mileage: int):
        self.make = make
        self.model = model
        self.year = year
        self.mileage = mileage

    def save_to_file(self):
        with open('maintenance_records.txt', 'a') as f:
            f.write(json.dumps(self.__dict__) + '\n')

class MaintenanceRecord:
    def __init__(self, vehicle_id: str, task: str, date: str, mileage: int):
        self.vehicle_id = vehicle_id
        self.task = task
        self.date = date
        self.mileage = mileage

    def save_to_file(self):
        with open('maintenance_records.txt', 'a') as f:
            f.write(json.dumps(self.__dict__) + '\n')

class VehicleMaintenanceTracker:
    def __init__(self):
        self.users = self.load_users()
        self.vehicles = []
        self.maintenance_records = self.load_maintenance_records()

    def load_users(self):
        if not os.path.exists('users.txt'):
            return []
        with open('users.txt', 'r') as f:
            return [line.strip().split('|') for line in f.readlines()]

    def load_maintenance_records(self):
        if not os.path.exists('maintenance_records.txt'):
            return []
        with open('maintenance_records.txt', 'r') as f:
            return [json.loads(line.strip()) for line in f.readlines()]

    def register_user(self, username: str, password: str):
        user = User(username, password)
        user.save_to_file()
        self.users.append((username, password))

    def login_user(self, username: str, password: str):
        return (username, password) in self.users

    def add_vehicle(self, make: str, model: str, year: int, mileage: int):
        vehicle = Vehicle(make, model, year, mileage)
        vehicle.save_to_file()
        self.vehicles.append(vehicle)

    def add_maintenance_record(self, vehicle_id: str, task: str, date: str, mileage: int):
        record = MaintenanceRecord(vehicle_id, task, date, mileage)
        record.save_to_file()
        self.maintenance_records.append(record.__dict__)

    def get_maintenance_history(self, vehicle_id: str):
        return [record for record in self.maintenance_records if record['vehicle_id'] == vehicle_id]

tracker = VehicleMaintenanceTracker()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if tracker.login_user(username, password):
            session['username'] = username
            return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        tracker.register_user(username, password)
        return redirect(url_for('login'))
    return render_template('registration.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        make = request.form['make']
        model = request.form['model']
        year = int(request.form['year'])
        mileage = int(request.form['mileage'])
        tracker.add_vehicle(make, model, year, mileage)
    return render_template('dashboard.html', vehicles=tracker.vehicles)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8686, debug=False)
