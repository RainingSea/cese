from flask import Flask, render_template, request, redirect, url_for, session
from user import User
from medical_info import MedicalInfo
from appointment import Appointment

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def load_users():
    users = {}
    with open('users.txt', 'r') as file:
        for line in file:
            username, password = line.strip().split('|')
            users[username] = password
    return users

def load_medical_info():
    medical_info = {}
    with open('medical_info.txt', 'r') as file:
        for line in file:
            username, diagnoses, medications, treatments = line.strip().split('|')
            medical_info[username] = MedicalInfo(username)
            medical_info[username].diagnoses = diagnoses.split(',')
            medical_info[username].medications = medications.split(',')
            medical_info[username].treatments = treatments.split(',')
    return medical_info

def load_appointments():
    appointments = {}
    with open('appointments.txt', 'r') as file:
        for line in file:
            username, reminders = line.strip().split('|')
            appointments[username] = Appointment(username)
            appointments[username].reminders = reminders.split(',')
    return appointments

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
    return render_template('registration.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if request.method == 'POST':
        username = session['username']
        medical_info = MedicalInfo(username)
        if 'add_diagnosis' in request.form:
            medical_info.add_diagnosis(request.form['diagnosis'])
        elif 'add_medication' in request.form:
            medical_info.add_medication(request.form['medication'])
        elif 'add_treatment' in request.form:
            medical_info.add_treatment(request.form['treatment'])
        medical_info.save()
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run(port=8638, debug=False)
