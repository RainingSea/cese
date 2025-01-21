from flask import Flask, render_template, request, redirect, url_for, session
from user import User
from medical_info import MedicalInfo
from appointment import Appointment
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

DATA_DIR = './data/'
USER_FILE = os.path.join(DATA_DIR, 'users.txt')
MEDICAL_INFO_FILE = os.path.join(DATA_DIR, 'medical_info.txt')
APPOINTMENTS_FILE = os.path.join(DATA_DIR, 'appointments.txt')

def load_users():
    users = {}
    if os.path.exists(USER_FILE):
        with open(USER_FILE, 'r') as file:
            for line in file:
                username, password = line.strip().split('|')
                users[username] = password
    return users

def load_medical_info():
    medical_info = {}
    if os.path.exists(MEDICAL_INFO_FILE):
        with open(MEDICAL_INFO_FILE, 'r') as file:
            for line in file:
                username, diagnoses, medications, treatments = line.strip().split('|')
                medical_info[username] = MedicalInfo(diagnoses.split(','), medications.split(','), treatments.split(','))
    return medical_info

def load_appointments():
    appointments = {}
    if os.path.exists(APPOINTMENTS_FILE):
        with open(APPOINTMENTS_FILE, 'r') as file:
            for line in file:
                username, date, time = line.strip().split('|')
                if username not in appointments:
                    appointments[username] = []
                appointments[username].append(Appointment(date, time))
    return appointments

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        with open(USER_FILE, 'a') as file:
            file.write(f"{username}|{password}\n")
        return redirect(url_for('login'))
    return render_template('registration.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if request.method == 'POST':
        if 'add_medical_info' in request.form:
            diagnoses = request.form.getlist('diagnoses')
            medications = request.form.getlist('medications')
            treatments = request.form.getlist('treatments')
            medical_info = MedicalInfo(diagnoses, medications, treatments)
            with open(MEDICAL_INFO_FILE, 'a') as file:
                file.write(f"{session['username']}|{','.join(diagnoses)}|{','.join(medications)}|{','.join(treatments)}\n")
        elif 'set_appointment' in request.form:
            date = request.form['date']
            time = request.form['time']
            appointment = Appointment(date, time)
            with open(APPOINTMENTS_FILE, 'a') as file:
                file.write(f"{session['username']}|{date}|{time}\n")
        return redirect(url_for('dashboard'))
    return render_template('dashboard.html')

@app.route('/login', methods=['POST'])
def do_login():
    users = load_users()
    username = request.form['username']
    password = request.form['password']
    if username in users and users[username] == password:
        session['username'] = username
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=9042, debug=False)
