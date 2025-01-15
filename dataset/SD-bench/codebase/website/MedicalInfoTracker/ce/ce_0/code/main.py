from flask import Flask, render_template, request, redirect, session, url_for
import json
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def to_dict(self) -> dict:
        return {'username': self.username, 'password': self.password}

class MedicalInfo:
    def __init__(self, diagnosis: str, medication: str, treatment: str):
        self.diagnosis = diagnosis
        self.medication = medication
        self.treatment = treatment

    def to_dict(self) -> dict:
        return {'diagnosis': self.diagnosis, 'medication': self.medication, 'treatment': self.treatment}

class Appointment:
    def __init__(self, date: str, time: str, description: str):
        self.date = date
        self.time = time
        self.description = description

    def to_dict(self) -> dict:
        return {'date': self.date, 'time': self.time, 'description': self.description}

class MedicalInfoTracker:
    def __init__(self):
        self.users = []
        self.medical_info = []
        self.appointments = []
        self.load_data()

    def register(self, username: str, password: str) -> bool:
        if any(user.username == username for user in self.users):
            return False
        new_user = User(username, password)
        self.users.append(new_user)
        self.save_data()
        return True

    def login(self, username: str, password: str) -> bool:
        for user in self.users:
            if user.username == username and user.password == password:
                return True
        return False

    def add_medical_info(self, info: MedicalInfo):
        self.medical_info.append(info)
        self.save_data()

    def set_appointment(self, appointment: Appointment):
        self.appointments.append(appointment)
        self.save_data()

    def load_data(self):
        if os.path.exists('users.txt'):
            with open('users.txt', 'r') as f:
                for line in f:
                    username, password = line.strip().split('|')
                    self.users.append(User(username, password))
        if os.path.exists('medical_info.txt'):
            with open('medical_info.txt', 'r') as f:
                for line in f:
                    diagnosis, medication, treatment = line.strip().split('|')
                    self.medical_info.append(MedicalInfo(diagnosis, medication, treatment))
        if os.path.exists('appointments.txt'):
            with open('appointments.txt', 'r') as f:
                for line in f:
                    date, time, description = line.strip().split('|')
                    self.appointments.append(Appointment(date, time, description))

    def save_data(self):
        with open('users.txt', 'w') as f:
            for user in self.users:
                f.write(f"{user.username}|{user.password}\n")
        with open('medical_info.txt', 'w') as f:
            for info in self.medical_info:
                f.write(f"{info.diagnosis}|{info.medication}|{info.treatment}\n")
        with open('appointments.txt', 'w') as f:
            for appointment in self.appointments:
                f.write(f"{appointment.date}|{appointment.time}|{appointment.description}\n")

tracker = MedicalInfoTracker()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if tracker.login(username, password):
            session['username'] = username
            return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if tracker.register(username, password):
            return redirect(url_for('login'))
    return render_template('registration.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    user_medical_info = tracker.medical_info  # Fetch user's medical info here if needed
    user_appointments = tracker.appointments  # Fetch user's appointments here if needed
    return render_template('dashboard.html', medical_info=user_medical_info, appointments=user_appointments)

if __name__ == '__main__':
    app.run(port=8635, debug=False)
