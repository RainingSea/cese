from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

class UserManager:
    def __init__(self):
        self.users = self.load_users()

    def load_users(self):
        if not os.path.exists('users.txt'):
            return []
        with open('users.txt', 'r') as file:
            return [line.strip().split('|') for line in file.readlines()]

    def register(self, username: str, password: str) -> bool:
        for user in self.users:
            if user[0] == username:
                return False
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
        if not os.path.exists('vehicles.txt'):
            return []
        with open('vehicles.txt', 'r') as file:
            return [line.strip().split('|') for line in file.readlines()]

    def add_vehicle(self, make: str, model: str, year: int, mileage: int) -> bool:
        self.vehicles.append([make, model, str(year), str(mileage)])
        self.save_vehicles()
        return True

    def save_vehicles(self):
        with open('vehicles.txt', 'w') as file:
            for vehicle in self.vehicles:
                file.write('|'.join(vehicle) + '\n')

    def get_vehicles(self):
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
        self.maintenance_records.append([str(vehicle_id), task, date])
        self.save_maintenance()
        return True

    def save_maintenance(self):
        with open('maintenance.txt', 'w') as file:
            for record in self.maintenance_records:
                file.write('|'.join(record) + '\n')

    def get_maintenance_history(self, vehicle_id: int):
        return [record for record in self.maintenance_records if int(record[0]) == vehicle_id]

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
            return "Registration failed. Username may already exist."
    return render_template('registration.html')

@app.route('/vehicle_info', methods=['GET', 'POST'])
def vehicle_info():
    if request.method == 'POST':
        make = request.form['make']
        model = request.form['model']
        year = int(request.form['year'])
        mileage = int(request.form['mileage'])
        vehicle_manager.add_vehicle(make, model, year, mileage)
        return redirect(url_for('vehicle_info'))
    vehicles = vehicle_manager.get_vehicles()
    return render_template('vehicle_info.html', vehicles=vehicles)

@app.route('/maintenance', methods=['GET', 'POST'])
def maintenance():
    if request.method == 'POST':
        vehicle_id = int(request.form['vehicle_id'])
        task = request.form['task']
        date = request.form['date']
        maintenance_manager.add_maintenance(vehicle_id, task, date)
        return redirect(url_for('maintenance'))
    records = maintenance_manager.maintenance_records
    return render_template('maintenance.html', records=records)

if __name__ == '__main__':
    user_manager = UserManager()
    vehicle_manager = VehicleManager()
    maintenance_manager = MaintenanceManager()
    app.run(port=8280, debug=False)
