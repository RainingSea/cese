from flask import Flask, render_template, request, redirect, url_for, session
from flask_session import Session
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

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
            return []
        with open('vehicles.txt', 'r') as file:
            return [line.strip().split('|') for line in file.readlines()]

    def add_vehicle(self, make: str, model: str, year: int, mileage: int) -> bool:
        self.vehicles.append([make, model, str(year), str(mileage)])
        with open('vehicles.txt', 'a') as file:
            file.write(f"{make}|{model}|{year}|{mileage}\n")
        return True

    def get_vehicles(self) -> list:
        return self.vehicles

class MaintenanceManager:
    def __init__(self):
        self.maintenance_records = self.load_maintenance()

    def load_maintenance(self):
        if not os.path.exists('maintenance.txt'):
            return []
        with open('maintenance.txt', 'r') as file:
            return [line.strip().split('|') for line in file.readlines()]

    def add_maintenance(self, vehicle_id: int, task: str, date: str, mileage: int) -> bool:
        self.maintenance_records.append([str(vehicle_id), task, date, str(mileage)])
        with open('maintenance.txt', 'a') as file:
            file.write(f"{vehicle_id}|{task}|{date}|{mileage}\n")
        return True

    def get_maintenance_history(self, vehicle_id: int) -> list:
        return [record for record in self.maintenance_records if int(record[0]) == vehicle_id]

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    user_manager = UserManager()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            return redirect(url_for('login'))
    return render_template('registration.html')

@app.route('/vehicle_info', methods=['GET', 'POST'])
def vehicle_info():
    vehicle_manager = VehicleManager()
    if request.method == 'POST':
        make = request.form['make']
        model = request.form['model']
        year = request.form['year']
        mileage = request.form['mileage']
        vehicle_manager.add_vehicle(make, model, int(year), int(mileage))
    vehicles = vehicle_manager.get_vehicles()
    return render_template('vehicle_info.html', vehicles=vehicles)

@app.route('/maintenance', methods=['GET', 'POST'])
def maintenance():
    maintenance_manager = MaintenanceManager()
    if request.method == 'POST':
        vehicle_id = request.form['vehicle_id']
        task = request.form['task']
        date = request.form['date']
        mileage = request.form['mileage']
        maintenance_manager.add_maintenance(int(vehicle_id), task, date, int(mileage))
    maintenance_records = maintenance_manager.maintenance_records
    return render_template('maintenance.html', maintenance_records=maintenance_records)

if __name__ == '__main__':
    app.run(port=8451, debug=False)
