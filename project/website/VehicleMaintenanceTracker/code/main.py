from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class UserManager:
    def __init__(self):
        self.users = self.load_users()

    def load_users(self):
        if not os.path.exists('users.txt'):
            return []
        with open('users.txt', 'r') as file:
            return [line.strip().split('|') for line in file.readlines()]

    def register(self, username: str, password: str) -> bool:
        if any(user[0] == username for user in self.users):
            return False
        self.users.append([username, password])
        with open('users.txt', 'a') as file:
            file.write(f"{username}|{password}\n")
        return True

    def login(self, username: str, password: str) -> bool:
        return any(user[0] == username and user[1] == password for user in self.users)

    def logout(self):
        session.pop('username', None)

class VehicleManager:
    def __init__(self):
        self.vehicles = self.load_vehicles()

    def load_vehicles(self):
        if not os.path.exists('vehicles.txt'):
            return []
        with open('vehicles.txt', 'r') as file:
            return [line.strip().split('|') for line in file.readlines()]

    def add_vehicle(self, make: str, model: str, year: int, mileage: int) -> bool:
        vehicle_data = f"{make}|{model}|{year}|{mileage}\n"
        with open('vehicles.txt', 'a') as file:
            file.write(vehicle_data)
        self.vehicles.append([make, model, str(year), str(mileage)])
        return True

    def view_vehicles(self):
        return self.vehicles

class MaintenanceManager:
    def __init__(self):
        self.maintenance_records = self.load_maintenance()

    def load_maintenance(self):
        if not os.path.exists('maintenance.txt'):
            return []
        with open('maintenance.txt', 'r') as file:
            return [line.strip().split('|') for line in file.readlines()]

    def add_maintenance(self, vehicle_id: int, task: str, date: str) -> bool:
        if not any(record[0] == str(vehicle_id) for record in self.maintenance_records):
            return False
        maintenance_data = f"{vehicle_id}|{task}|{date}\n"
        with open('maintenance.txt', 'a') as file:
            file.write(maintenance_data)
        self.maintenance_records.append([str(vehicle_id), task, date])
        return True

    def view_maintenance(self, vehicle_id: int):
        return [record for record in self.maintenance_records if int(record[0]) == vehicle_id]

user_manager = UserManager()
vehicle_manager = VehicleManager()
maintenance_manager = MaintenanceManager()

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
        else:
            error_message = "Registration failed. Username already exists."
            return render_template('registration.html', error=error_message)
    return render_template('registration.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    vehicles = vehicle_manager.view_vehicles()
    return render_template('dashboard.html', vehicles=vehicles)

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    if user_manager.login(username, password):
        session['username'] = username
        return redirect(url_for('dashboard'))
    return "Login failed. Check your username and password."

@app.route('/logout')
def logout():
    user_manager.logout()
    return redirect(url_for('login'))

@app.route('/vehicle_management', methods=['GET', 'POST'])
def vehicle_management():
    if request.method == 'POST':
        make = request.form['make']
        model = request.form['model']
        year = request.form['year']
        mileage = request.form['mileage']
        vehicle_manager.add_vehicle(make, model, year, mileage)
        return redirect(url_for('vehicle_management'))
    vehicles = vehicle_manager.view_vehicles()
    return render_template('vehicle_management.html', vehicles=vehicles)

@app.route('/maintenance_tracking', methods=['GET', 'POST'])
def maintenance_tracking():
    if request.method == 'POST':
        vehicle_id = request.form['vehicle_id']
        task = request.form['task']
        date = request.form['date']
        if maintenance_manager.add_maintenance(vehicle_id, task, date):
            return redirect(url_for('maintenance_tracking'))
        else:
            error_message = "Invalid vehicle ID. Maintenance record not added."
            records = maintenance_manager.maintenance_records
            return render_template('maintenance_tracking.html', records=records, error=error_message)
    maintenance_records = maintenance_manager.maintenance_records
    return render_template('maintenance_tracking.html', records=maintenance_records)

if __name__ == '__main__':
    app.run(port=8453, debug=False)
