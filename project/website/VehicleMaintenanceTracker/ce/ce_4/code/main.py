from flask import Flask, render_template, request, redirect, session
from user import User
from vehicle import Vehicle

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def load_users():
    users = []
    try:
        with open('users.txt', 'r') as file:
            for line in file:
                username, password = line.strip().split('|')
                users.append(User(username, password))
    except FileNotFoundError:
        pass
    return users

def load_vehicles():
    vehicles = []
    try:
        with open('vehicles.txt', 'r') as file:
            for line in file:
                make, model, year, mileage, records = line.strip().split('|')
                vehicle = Vehicle(make, model, int(year), int(mileage))
                if records:
                    records_list = records.split(';')
                    for record in records_list:
                        task, date = record.split(',')
                        vehicle.add_maintenance(task, date)
                vehicles.append(vehicle)
    except FileNotFoundError:
        pass
    return vehicles

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
        return redirect('/')
    return render_template('register.html')

@app.route('/vehicle_info', methods=['GET', 'POST'])
def vehicle_info():
    if request.method == 'POST':
        make = request.form['make']
        model = request.form['model']
        year = request.form['year']
        mileage = request.form['mileage']
        new_vehicle = Vehicle(make, model, int(year), int(mileage))
        new_vehicle.save()
        return redirect('/vehicle_info')
    return render_template('vehicle_info.html')

if __name__ == '__main__':
    app.run(port=8687, debug=False)
