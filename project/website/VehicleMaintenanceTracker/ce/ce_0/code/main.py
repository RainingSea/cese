from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class UserManager:
    def __init__(self):
        self.users = self.load_users()

    def load_users(self):
        if not os.path.exists('users.txt'):
            return {}
        with open('users.txt', 'r') as file:
            return {line.split('|')[0]: line.split('|')[1].strip() for line in file.readlines()}

    def register(self, username: str, password: str) -> bool:
        if username in self.users:
            return False
        self.users[username] = password
        with open('users.txt', 'a') as file:
            file.write(f"{username}|{password}\n")
        return True

    def login(self, username: str, password: str) -> bool:
        return self.users.get(username) == password

class VehicleManager:
    def __init__(self):
        self.vehicles = self.load_vehicles()

    def load_vehicles(self):
        if not os.path.exists('vehicles.txt'):
            return {}
        with open('vehicles.txt', 'r') as file:
            return {line.split('|')[0]: line.strip().split('|')[1:] for line in file.readlines()}

    def add_vehicle(self, make: str, model: str, year: int, mileage: int) -> bool:
        vehicle_id = f"{make}_{model}_{year}"
        if vehicle_id in self.vehicles:
            return False
        self.vehicles[vehicle_id] = [make, model, str(year), str(mileage)]
        with open('vehicles.txt', 'a') as file:
            file.write(f"{vehicle_id}|{make}|{model}|{year}|{mileage}\n")
        return True

    def get_vehicles(self):
        return self.vehicles

class MaintenanceManager:
    def __init__(self):
        self.maintenance_records = self.load_maintenance_records()

    def load_maintenance_records(self):
        if not os.path.exists('maintenance.txt'):
            return {}
        with open('maintenance.txt', 'r') as file:
            return {line.split('|')[0]: line.strip().split('|')[1:] for line in file.readlines()}

    def add_maintenance(self, vehicle_id: str, task: str, date: str) -> bool:
        if vehicle_id not in self.maintenance_records:
            self.maintenance_records[vehicle_id] = []
        self.maintenance_records[vehicle_id].append((task, date))
        with open('maintenance.txt', 'a') as file:
            file.write(f"{vehicle_id}|{task}|{date}\n")
        return True

    def get_maintenance_history(self, vehicle_id: str):
        return self.maintenance_records.get(vehicle_id, [])

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
        return "Registration failed. Username may already exist."
    return render_template('registration.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if request.method == 'POST':
        make = request.form['make']
        model = request.form['model']
        year = request.form['year']
        mileage = request.form['mileage']
        vehicle_manager.add_vehicle(make, model, year, mileage)
    vehicles = vehicle_manager.get_vehicles()
    return render_template('dashboard.html', vehicles=vehicles)

if __name__ == '__main__':
    app.run(port=8278, debug=False)
