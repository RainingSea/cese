from flask import Flask, render_template, request, redirect, session, url_for
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

def load_medical_info(username):
    medical_info = MedicalInfo([], [], [])
    try:
        with open('medical_info.txt', 'r') as file:
            for line in file:
                user, diagnoses, medications, treatments = line.strip().split('|')
                if user == username:
                    medical_info.diagnoses = diagnoses.split(',')
                    medical_info.medications = medications.split(',')
                    medical_info.treatments = treatments.split(',')
                    break
    except FileNotFoundError:
        pass
    return medical_info

def load_appointments(username):
    appointments = Appointment([])
    try:
        with open('appointments.txt', 'r') as file:
            for line in file:
                user, appointment_details = line.strip().split('|')
                if user == username:
                    appointments.appointments = appointment_details.split(',')
                    break
    except FileNotFoundError:
        pass
    return appointments

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = load_users()
        if username in users and users[username] == password:
            session['username'] = username
            return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = load_users()
        if username in users:
            return render_template('register.html', error="Username already exists.")
        with open('users.txt', 'a') as file:
            file.write(f"{username}|{password}\n")
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    username = session['username']
    medical_info = load_medical_info(username)
    appointments = load_appointments(username)

    if request.method == 'POST':
        if 'add_medical_info' in request.form:
            diagnosis = request.form['diagnosis']
            medication = request.form['medication']
            treatment = request.form['treatment']
            medical_info.add_diagnosis(diagnosis)
            medical_info.add_medication(medication)
            medical_info.add_treatment(treatment)
            medical_info.save(username)

        if 'edit_medical_info' in request.form:
            medical_info.diagnoses = request.form.getlist('diagnoses')
            medical_info.medications = request.form.getlist('medications')
            medical_info.treatments = request.form.getlist('treatments')
            medical_info.save(username)

        if 'add_appointment' in request.form:
            date = request.form['date']
            time = request.form['time']
            details = request.form['details']
            appointments.add_appointment(date, time, details)
            appointments.save(username)

    return render_template('dashboard.html', medical_info=medical_info, appointments=appointments)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8537, debug=False)
