from flask import Flask, render_template, request, redirect, url_for, session
from user import User
from vehicle import Vehicle
from maintenance_record import MaintenanceRecord

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Load users and vehicles from file
users = User.load_users()
vehicles = Vehicle.load_vehicles()

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

@app.route('/vehicle_info', methods=['GET', 'POST'])
def vehicle_info():
    if request.method == 'POST':
        make = request.form['make']
        model = request.form['model']
        year = int(request.form['year'])
        mileage = int(request.form['mileage'])
        new_vehicle = Vehicle(make, model, year, mileage)
        new_vehicle.save()
        return redirect(url_for('maintenance_tracking'))
    return render_template('vehicle_info.html')

@app.route('/maintenance_tracking', methods=['GET', 'POST'])
def maintenance_tracking():
    if request.method == 'POST':
        vehicle_id = int(request.form['vehicle_id'])
        task = request.form['task']
        date = request.form['date']
        new_record = MaintenanceRecord(vehicle_id, task, date)
        new_record.save()
    records = MaintenanceRecord.load_records()
    return render_template('maintenance_tracking.html', records=records)

@app.route('/view_maintenance_history/<int:vehicle_id>', methods=['GET'])
def view_maintenance_history(vehicle_id):
    records = MaintenanceRecord.load_records()
    vehicle_records = [record for record in records if record.vehicle_id == vehicle_id]
    return render_template('maintenance_history.html', records=vehicle_records)

@app.route('/send_reminders_and_notifications', methods=['GET'])
def send_reminders_and_notifications():
    records = MaintenanceRecord.load_records()
    # Here we would implement the logic to send reminders based on the records
    # For now, we will just return a simple message
    return "Reminders and notifications sent!"

@app.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/update_or_delete_maintenance_records', methods=['POST'])
def update_or_delete_maintenance_records():
    if request.method == 'POST':
        action = request.form['action']
        record_id = int(request.form['record_id'])
        records = MaintenanceRecord.load_records()
        if action == 'delete':
            records = [record for record in records if record.vehicle_id != record_id]
            with open('maintenance_records.txt', 'w') as file:
                for record in records:
                    file.write(f"{record.vehicle_id}|{record.task}|{record.date}\n")
        # Additional logic for updating records can be added here
    return redirect(url_for('maintenance_tracking'))

@app.route('/dashboard', methods=['GET'])
def dashboard():
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run(port=8562, debug=False)
