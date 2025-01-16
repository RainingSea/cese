from flask import Flask, render_template, request, redirect, url_for, session
from user import User
from vehicle import Vehicle
from maintenance_record import MaintenanceRecord

app = Flask(__name__)
app.secret_key = 'supersecretkey'

def load_users():
    users = []
    with open('users.txt', 'r') as file:
        for line in file:
            username, password = line.strip().split('|')
            users.append(User(username, password))
    return users

def load_vehicles():
    vehicles = []
    with open('vehicles.txt', 'r') as file:
        for line in file:
            make, model, year, mileage = line.strip().split('|')
            vehicles.append(Vehicle(make, model, int(year), int(mileage)))
    return vehicles

def load_maintenance_records():
    records = []
    with open('maintenance.txt', 'r') as file:
        for line in file:
            vehicle_id, task, date = line.strip().split('|')
            records.append(MaintenanceRecord(int(vehicle_id), task, date))
    return records

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = load_users()
        for user in users:
            if user.username == username and user.password == password:
                session['username'] = username
                return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'username' not in session:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        make = request.form['make']
        model = request.form['model']
        year = request.form['year']
        mileage = request.form['mileage']
        vehicle = Vehicle(make, model, int(year), int(mileage))
        vehicle.save()
    
    vehicles = load_vehicles()
    return render_template('dashboard.html', vehicles=vehicles)

@app.route('/history')
def history():
    if 'username' not in session:
        return redirect(url_for('index'))
    
    records = load_maintenance_records()
    return render_template('history.html', records=records)

if __name__ == '__main__':
    app.run(port=8685, debug=False)
