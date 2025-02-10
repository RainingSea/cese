from flask import Flask, render_template, request, redirect, url_for, session
from user import User
from vehicle import Vehicle
from maintenance import Maintenance

app = Flask(__name__)
app.secret_key = 'supersecretkey'

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User(username, password)
        user.save()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/vehicle_info', methods=['GET', 'POST'])
def vehicle_info():
    if request.method == 'POST':
        make = request.form['make']
        model = request.form['model']
        year = int(request.form['year'])
        mileage = int(request.form['mileage'])
        vehicle = Vehicle(make, model, year, mileage)
        vehicle.save()
        return redirect(url_for('maintenance'))
    return render_template('vehicle_info.html')

@app.route('/maintenance', methods=['GET', 'POST'])
def maintenance():
    if request.method == 'POST':
        task = request.form['task']
        date = request.form['date']
        vehicle_id = int(request.form['vehicle_id'])
        maintenance_task = Maintenance(task, date, vehicle_id)
        maintenance_task.save()
    return render_template('maintenance.html')

if __name__ == '__main__':
    app.run(port=8684, debug=False)
