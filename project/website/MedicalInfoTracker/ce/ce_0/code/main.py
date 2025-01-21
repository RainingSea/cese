from flask import Flask, render_template, request, redirect, url_for, session
from user import User
from medical_info import MedicalInfo
from appointment import Appointment

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Load user data
def load_users():
    users = {}
    with open('users.txt', 'r') as file:
        for line in file:
            username, password = line.strip().split('|')
            users[username] = password
    return users

# Load medical information
def load_medical_info():
    medical_info = MedicalInfo()
    with open('medical_info.txt', 'r') as file:
        for line in file:
            diagnosis, medication, treatment = line.strip().split('|')
            medical_info.add_diagnosis(diagnosis)
            medical_info.add_medication(medication)
            medical_info.add_treatment(treatment)
    return medical_info

# Load appointments
def load_appointments():
    appointment = Appointment()
    with open('appointments.txt', 'r') as file:
        for line in file:
            date, time, description = line.strip().split('|')
            appointment.set_appointment(date, time, description)
    return appointment

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User()
        if user.register(username, password):
            return redirect(url_for('login'))
    return render_template('registration.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if request.method == 'POST':
        # Handle medical info submission
        pass
    return render_template('dashboard.html')

@app.route('/history')
def history():
    return render_template('history.html')

if __name__ == '__main__':
    app.run(port=9040, debug=False)
