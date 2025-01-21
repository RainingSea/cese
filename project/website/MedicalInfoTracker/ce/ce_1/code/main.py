from flask import Flask, render_template, request, redirect, url_for, session
from bcrypt import hashpw, gensalt, checkpw
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = hashpw(password.encode('utf-8'), gensalt()).decode('utf-8')

    def save(self):
        with open('users.txt', 'a') as f:
            f.write(f"{self.username}|{self.password}\n")

    @staticmethod
    def load(username: str):
        with open('users.txt', 'r') as f:
            for line in f:
                user_data = line.strip().split('|')
                if user_data[0] == username:
                    return User(user_data[0], user_data[1])
        return None

class MedicalInfo:
    def __init__(self, diagnoses: list = None, medications: list = None, treatments: list = None):
        self.diagnoses = diagnoses if diagnoses else []
        self.medications = medications if medications else []
        self.treatments = treatments if treatments else []

    def add_diagnosis(self, diagnosis: str):
        self.diagnoses.append(diagnosis)

    def add_medication(self, medication: str):
        self.medications.append(medication)

    def add_treatment(self, treatment: str):
        self.treatments.append(treatment)

    def save(self):
        with open('medical_info.txt', 'a') as f:
            f.write(f"{'|'.join(self.diagnoses)}|{'|'.join(self.medications)}|{'|'.join(self.treatments)}\n")

    @staticmethod
    def load():
        medical_info = MedicalInfo()
        if os.path.exists('medical_info.txt'):
            with open('medical_info.txt', 'r') as f:
                for line in f:
                    diagnoses, medications, treatments = line.strip().split('|')
                    medical_info.diagnoses = diagnoses.split('|') if diagnoses else []
                    medical_info.medications = medications.split('|') if medications else []
                    medical_info.treatments = treatments.split('|') if treatments else []
        return medical_info

class Appointment:
    def __init__(self, date: str, time: str, description: str):
        self.date = date
        self.time = time
        self.description = description

    def save(self):
        with open('appointments.txt', 'a') as f:
            f.write(f"{self.date}|{self.time}|{self.description}\n")

    @staticmethod
    def load():
        appointments = []
        if os.path.exists('appointments.txt'):
            with open('appointments.txt', 'r') as f:
                for line in f:
                    date, time, description = line.strip().split('|')
                    appointments.append(Appointment(date, time, description))
        return appointments

class App:
    def register(self, username: str, password: str):
        user = User(username, password)
        user.save()

    def login(self, username: str, password: str) -> bool:
        user = User.load(username)
        if user and checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            return True
        return False

    def add_medical_info(self, info: MedicalInfo):
        info.save()

    def set_appointment(self, appointment: Appointment):
        appointment.save()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        app_instance = App()
        if app_instance.login(username, password):
            session['username'] = username
            return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        app_instance = App()
        app_instance.register(username, password)
        return redirect(url_for('login'))
    return render_template('registration.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    medical_info = MedicalInfo.load()
    if request.method == 'POST':
        diagnosis = request.form.get('diagnosis')
        medication = request.form.get('medication')
        treatment = request.form.get('treatment')
        if diagnosis:
            medical_info.add_diagnosis(diagnosis)
        if medication:
            medical_info.add_medication(medication)
        if treatment:
            medical_info.add_treatment(treatment)
        medical_info.save()
    return render_template('dashboard.html', medical_info=medical_info)

if __name__ == '__main__':
    app.run(port=9041, debug=False)
