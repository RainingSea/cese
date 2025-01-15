from flask import Flask, render_template, request, redirect, url_for, session
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def save(self):
        with open('users.txt', 'a') as f:
            f.write(f"{self.username}|{self.password}\n")

class MedicalInfo:
    def __init__(self, diagnoses: list, medications: list, treatments: list):
        self.diagnoses = diagnoses
        self.medications = medications
        self.treatments = treatments

    def add_diagnosis(self, diagnosis: str):
        self.diagnoses.append(diagnosis)

    def add_medication(self, medication: str):
        self.medications.append(medication)

    def add_treatment(self, treatment: str):
        self.treatments.append(treatment)

    def save(self):
        with open('medical_info.txt', 'a') as f:
            f.write(json.dumps({
                'diagnoses': self.diagnoses,
                'medications': self.medications,
                'treatments': self.treatments
            }) + '\n')

class Appointment:
    def __init__(self, date_time: str, description: str):
        self.date_time = date_time
        self.description = description

    def save(self):
        with open('appointments.txt', 'a') as f:
            f.write(f"{self.date_time}|{self.description}\n")

class App:
    def register_user(self, username: str, password: str):
        user = User(username, password)
        user.save()

    def login_user(self, username: str, password: str) -> bool:
        with open('users.txt', 'r') as f:
            users = f.readlines()
            for line in users:
                u, p = line.strip().split('|')
                if u == username and p == password:
                    return True
        return False

    def add_medical_info(self, user: User, info: MedicalInfo):
        info.save()

    def set_appointment(self, user: User, appointment: Appointment):
        appointment.save()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        app_instance = App()
        app_instance.register_user(username, password)
        return redirect(url_for('login'))
    return render_template('registration.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if request.method == 'POST':
        if 'username' in session:
            # Handle medical info and appointments here
            return redirect(url_for('dashboard'))
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run(port=8636, debug=False)
