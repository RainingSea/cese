from flask import Flask, render_template, request, redirect, url_for, session
import json
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class UserManager:
    def __init__(self):
        self.users = self.load_users()

    def load_users(self):
        if os.path.exists('users.txt'):
            with open('users.txt', 'r') as file:
                return [line.strip().split('|') for line in file.readlines()]
        return []

    def register(self, username: str, password: str) -> bool:
        for user in self.users:
            if user[0] == username:
                return False  # User already exists
        self.users.append([username, password])
        self.save_users()
        return True

    def save_users(self):
        with open('users.txt', 'w') as file:
            for user in self.users:
                file.write('|'.join(user) + '\n')

    def login(self, username: str, password: str) -> bool:
        for user in self.users:
            if user[0] == username and user[1] == password:
                return True
        return False

class VehicleManager:
    def __init__(self):
        self.vehicles = self.load_vehicles()

    def load_vehicles(self):
        if os.path.exists('vehicles.txt'):
            with open('vehicles.txt', 'r') as file:
                return [line.strip().split('|') for line in file.readlines()]
        return []

    def add_vehicle(self, make: str, model: str, year: int, mileage: int) -> bool:
        self.vehicles.append([make, model, str(year), str(mileage)])
        self.save_vehicles()
        return True

    def save_vehicles(self):
        with open('vehicles.txt', 'w') as file:
            for vehicle in self.vehicles:
                file.write('|'.join(vehicle) + '\n')

class MaintenanceManager:
    def __init__(self):
        self.maintenance_records = self.load_records()

    def load_records(self):
        if os.path.exists('maintenance.txt'):
            with open('maintenance.txt', 'r') as file:
                return [line.strip().split('|') for line in file.readlines()]
        return []

    def add_record(self, vehicle_id: int, task: str, date: str) -> bool:
        self.maintenance_records.append([str(vehicle_id), task, date])
        self.save_records()
        return True

    def save_records(self):
        with open('maintenance.txt', 'w') as file:
            for record in self.maintenance_records:
                file.write('|'.join(record) + '\n')

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
            return "User already exists."
    return render_template('registration.html')

@app.route('/vehicle', methods=['GET', 'POST'])
def vehicle_input():
    if request.method == 'POST':
        make = request.form['make']
        model = request.form['model']
        year = request.form['year']
        mileage = request.form['mileage']
        vehicle_manager.add_vehicle(make, model, int(year), int(mileage))
        return redirect(url_for('vehicle_input'))
    return render_template('vehicle_input.html')

@app.route('/maintenance', methods=['GET', 'POST'])
def maintenance_tracking():
    if request.method == 'POST':
        vehicle_id = request.form['vehicle_id']
        task = request.form['task']
        date = request.form['date']
        maintenance_manager.add_record(int(vehicle_id), task, date)
        return redirect(url_for('maintenance_tracking'))
    return render_template('maintenance_tracking.html')

if __name__ == '__main__':
    app.run(port=8279, debug=False)
