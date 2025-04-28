from flask import Flask, render_template, request, redirect, url_for, session
from flask_session import Session

class UserManager:
    def __init__(self):
        self.users = self.load_users()

    def load_users(self):
        users = []
        with open('users.txt', 'r') as file:
            for line in file:
                username, password = line.strip().split(',')
                users.append((username, password))
        return users

    def register(self, username: str, password: str) -> bool:
        if any(user[0] == username for user in self.users):
            return False
        self.users.append((username, password))
        with open('users.txt', 'a') as file:
            file.write(f"{username},{password}\n")
        return True

    def login(self, username: str, password: str) -> bool:
        return (username, password) in self.users

class VehicleManager:
    def __init__(self):
        self.vehicles = self.load_vehicles()

    def load_vehicles(self):
        vehicles = []
        with open('vehicles.txt', 'r') as file:
            for line in file:
                username, make, model, year, mileage = line.strip().split(',')
                vehicles.append((username, make, model, int(year), int(mileage)))
        return vehicles

    def add_vehicle(self, username: str, make: str, model: str, year: int, mileage: int) -> bool:
        self.vehicles.append((username, make, model, year, mileage))
        with open('vehicles.txt', 'a') as file:
            file.write(f"{username},{make},{model},{year},{mileage}\n")
        return True

    def get_vehicles(self, username: str) -> list:
        return [vehicle for vehicle in self.vehicles if vehicle[0] == username]

class MaintenanceManager:
    def __init__(self):
        self.maintenance_records = self.load_maintenance()

    def load_maintenance(self):
        records = []
        with open('maintenance.txt', 'r') as file:
            for line in file:
                username, vehicle_id, task, date, status = line.strip().split(',')
                records.append((username, int(vehicle_id), task, date, status))
        return records

    def add_maintenance(self, username: str, vehicle_id: int, task: str, date: str, status: str) -> bool:
        self.maintenance_records.append((username, vehicle_id, task, date, status))
        with open('maintenance.txt', 'a') as file:
            file.write(f"{username},{vehicle_id},{task},{date},{status}\n")
        return True

    def get_maintenance_history(self, username: str) -> list:
        return [record for record in self.maintenance_records if record[0] == username]

app = Flask(__name__)
app.secret_key = 'your_secret_key'
Session(app)

user_manager = UserManager()
vehicle_manager = VehicleManager()
maintenance_manager = MaintenanceManager()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.login(username, password):
            session['username'] = username
            return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            return redirect(url_for('login'))
    return render_template('registration.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    vehicles = vehicle_manager.get_vehicles(session['username'])
    maintenance_history = maintenance_manager.get_maintenance_history(session['username'])
    return render_template('dashboard.html', vehicles=vehicles, maintenance_history=maintenance_history)

if __name__ == '__main__':
    app.run(port=8450, debug=False)
