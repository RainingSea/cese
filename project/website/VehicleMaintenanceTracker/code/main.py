from flask import Flask, render_template, request, redirect, session, flash
import json
from data_manager import DataManager
from user import User
from vehicle import Vehicle
from maintenance import Maintenance
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure key

data_manager = DataManager()

@app.route('/', methods=['GET', 'POST'])
def index():
    """Handles user login."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = data_manager.load_users()
        for user in users:
            if user.username == username and user.password == password:
                session['username'] = username
                return redirect('/dashboard')
        flash('Invalid username or password')  # Feedback for invalid login
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    """Displays the dashboard with vehicle information."""
    if 'username' not in session:
        return redirect('/')
    vehicles = data_manager.load_vehicles()
    return render_template('dashboard.html', vehicles=vehicles)

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Handles user registration."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = data_manager.load_users()
        if any(user.username == username for user in users):
            flash('Username already exists. Please choose a different one.')  # Feedback for existing username
        else:
            new_user = User(username, password)
            data_manager.save_user(new_user)
            return redirect('/')
    return render_template('registration.html')

@app.route('/vehicle_info', methods=['GET', 'POST'])
def vehicle_info():
    """Handles vehicle information submission."""
    if request.method == 'POST':
        make = request.form['make']
        model = request.form['model']
        year = int(request.form['year'])
        mileage = int(request.form['mileage'])
        
        # Validate vehicle information
        if not (year > 1885 and mileage >= 0):  # Year must be greater than 1885 and mileage cannot be negative
            flash('Invalid vehicle information. Please check your inputs.')  # Feedback for invalid input
            return render_template('vehicle_info.html')

        new_vehicle = Vehicle(make, model, year, mileage)
        data_manager.save_vehicle(new_vehicle)
        return redirect('/maintenance_tracking')
    return render_template('vehicle_info.html')

@app.route('/maintenance_tracking', methods=['GET', 'POST'])
def maintenance_tracking():
    """Handles maintenance tracking submission."""
    if request.method == 'POST':
        vehicle_id = int(request.form['vehicle_id'])
        task = request.form['task']
        date = request.form['date']
        mileage = int(request.form['mileage'])
        
        # Validate maintenance task information
        if not (vehicle_id and task and date and mileage >= 0):  # Ensure all fields are filled and mileage is non-negative
            flash('Please fill all fields correctly.')  # Feedback for invalid input
            return render_template('maintenance_tracking.html')

        new_maintenance = Maintenance(vehicle_id, task, date, mileage)
        data_manager.save_maintenance(new_maintenance)
        return redirect('/maintenance_history?vehicle_id=' + str(vehicle_id))
    return render_template('maintenance_tracking.html')

@app.route('/maintenance_history')
def maintenance_history():
    """Displays the maintenance history for a specific vehicle."""
    if 'username' not in session:
        return redirect('/')
    vehicle_id = request.args.get('vehicle_id')
    maintenance_records = data_manager.load_maintenance(vehicle_id)
    return render_template('maintenance_history.html', records=maintenance_records)

@app.route('/send_reminders')
def send_reminders():
    """Sends reminders for upcoming maintenance tasks."""
    vehicles = data_manager.load_vehicles()
    for vehicle in vehicles:
        maintenance_records = data_manager.load_maintenance(vehicle.vehicle_id)
        for record in maintenance_records:
            maintenance_date = datetime.strptime(record.date, '%Y-%m-%d')
            if maintenance_date <= datetime.now() + timedelta(days=7):
                # Here you would send an email or notification
                print(f"Reminder: Maintenance task '{record.task}' for vehicle ID {vehicle.vehicle_id} is due on {record.date}.")
    return redirect('/dashboard')

@app.route('/logout')
def logout():
    """Handles user logout."""
    session.pop('username', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(port=8688, debug=False)
