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
        self.save_users()
        return True

    def save_users(self):
        with open('users.txt', 'w') as file:
            for user in self.users:
                file.write('|'.join(user) + '\n')

    def login(self, username: str, password: str) -> bool:
        for user in self.users:
            if user[0] == username and user[1] == password:
                session['username'] = username
                return True
        return False

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
        if mileage < 0:
            return False
        self.vehicles.append([make, model, str(year), str(mileage)])
        self.save_vehicles()
        return True

    def save_vehicles(self):
        with open('vehicles.txt', 'w') as file:
            for vehicle in self.vehicles:
                file.write('|'.join(vehicle) + '\n')

    def update_vehicle(self, vehicle_id: int, make: str, model: str, year: int, mileage: int) -> bool:
        if 0 <= vehicle_id < len(self.vehicles):
            if mileage < 0:
                return False
            self.vehicles[vehicle_id] = [make, model, str(year), str(mileage)]
            self.save_vehicles()
            return True
        return False

    def delete_vehicle(self, vehicle_id: int) -> bool:
        if 0 <= vehicle_id < len(self.vehicles):
            del self.vehicles[vehicle_id]
            self.save_vehicles()
            return True
        return False

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
        if not task or not date:
            return False  # Validation for required fields
        self.maintenance_records.append([str(vehicle_id), task, date])
        self.save_maintenance()
        return True

    def save_maintenance(self):
        with open('maintenance.txt', 'w') as file:
            for record in self.maintenance_records:
                file.write('|'.join(record) + '\n')

    def update_maintenance(self, record_id: int, task: str, date: str) -> bool:
        if 0 <= record_id < len(self.maintenance_records):
            if not task or not date:
                return False  # Validation for required fields
            self.maintenance_records[record_id] = [self.maintenance_records[record_id][0], task, date]
            self.save_maintenance()
            return True
        return False

    def delete_maintenance(self, record_id: int) -> bool:
        if 0 <= record_id < len(self.maintenance_records):
            del self.maintenance_records[record_id]
            self.save_maintenance()
            return True
        return False

    def view_maintenance(self, vehicle_id: int):
        return [record for record in self.maintenance_records if int(record[0]) == vehicle_id]

    def maintenance_history(self, vehicle_id: int):
        return self.view_maintenance(vehicle_id)

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
        else:
            return render_template('registration.html', error="User already exists.")
    return render_template('registration.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    vehicle_manager = VehicleManager()
    vehicles = vehicle_manager.view_vehicles()
    return render_template('dashboard.html', vehicles=vehicles)

@app.route('/login', methods=['POST'])
def do_login():
    user_manager = UserManager()
    username = request.form['username']
    password = request.form['password']
    if user_manager.login(username, password):
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/logout')
def do_logout():
    user_manager = UserManager()
    user_manager.logout()
    return redirect(url_for('login'))

@app.route('/maintenance/<int:vehicle_id>')
def view_maintenance(vehicle_id):
    maintenance_manager = MaintenanceManager()
    records = maintenance_manager.maintenance_history(vehicle_id)
    return render_template('maintenance.html', records=records)

if __name__ == '__main__':
    app.run(port=8281, debug=False)
