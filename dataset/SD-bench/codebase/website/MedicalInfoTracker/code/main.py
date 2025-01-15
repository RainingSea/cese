from flask import Flask, render_template, request, redirect, session
from user import User
from medical_info import MedicalInfo
from appointment import Appointment
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Load users from users.txt
def load_users():
    users = []
    if os.path.exists('users.txt'):
        with open('users.txt', 'r') as file:
            for line in file:
                username, password = line.strip().split('|')
                users.append(User(username, password))
    return users

# Load medical information from medical_info.txt
def load_medical_info():
    medical_info = []
    if os.path.exists('medical_info.txt'):
        with open('medical_info.txt', 'r') as file:
            for line in file:
                diagnoses, medications, treatments = line.strip().split('|')
                medical_info.append(MedicalInfo(diagnoses.split(','), medications.split(','), treatments.split(',')))
    return medical_info

# Load appointments from appointments.txt
def load_appointments():
    appointments = []
    if os.path.exists('appointments.txt'):
        with open('appointments.txt', 'r') as file:
            for line in file:
                date, time, description = line.strip().split('|')
                appointments.append(Appointment(date, time, description))
    return appointments

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = load_users()
        for user in users:
            if user.username == username and user.password == password:
                session['username'] = username
                return redirect('/dashboard')
        return "Invalid username or password!"
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = load_users()
        if any(user.username == username for user in users):
            return "Username already exists!"
        new_user = User(username, password)
        new_user.save()
        return redirect('/')
    return render_template('registration.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'username' not in session:
        return redirect('/')
    
    medical_info = load_medical_info()
    appointments = load_appointments()

    if request.method == 'POST':
        if 'add_medical_info' in request.form:
            diagnoses = request.form['diagnoses'].split(',')
            medications = request.form['medications'].split(',')
            treatments = request.form['treatments'].split(',')
            medical_info_entry = MedicalInfo(diagnoses, medications, treatments)
            medical_info_entry.save()
        
        if 'set_appointment' in request.form:
            date = request.form['date']
            time = request.form['time']
            description = request.form['description']
            appointment = Appointment(date, time, description)
            appointment.save()
    
    return render_template('dashboard.html', username=session['username'], medical_info=medical_info, appointments=appointments)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(port=8640, debug=False)
