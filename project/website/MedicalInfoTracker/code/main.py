from flask import Flask, render_template, request, redirect, url_for, session, flash
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

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

    @staticmethod
    def username_exists(username: str) -> bool:
        with open('users.txt', 'r') as f:
            for line in f:
                if line.strip().split('|')[0] == username:
                    return True
        return False

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

    def save(self, username: str):
        with open('medical_info.txt', 'a') as f:
            for diagnosis in self.diagnoses:
                f.write(f"{username}|diagnosis|{diagnosis}\n")
            for medication in self.medications:
                f.write(f"{username}|medication|{medication}\n")
            for treatment in self.treatments:
                f.write(f"{username}|treatment|{treatment}\n")

    @staticmethod
    def load(username: str):
        medical_info = MedicalInfo()
        with open('medical_info.txt', 'r') as f:
            for line in f:
                info_data = line.strip().split('|')
                if info_data[0] == username:
                    if info_data[1] == 'diagnosis':
                        medical_info.add_diagnosis(info_data[2])
                    elif info_data[1] == 'medication':
                        medical_info.add_medication(info_data[2])
                    elif info_data[1] == 'treatment':
                        medical_info.add_treatment(info_data[2])
        return medical_info

    def edit_medical_info(self, username: str, info_type: str, old_value: str, new_value: str):
        if info_type == 'diagnosis':
            self.diagnoses = [new_value if d == old_value else d for d in self.diagnoses]
        elif info_type == 'medication':
            self.medications = [new_value if m == old_value else m for m in self.medications]
        elif info_type == 'treatment':
            self.treatments = [new_value if t == old_value else t for t in self.treatments]
        self.save(username)

    def delete_medical_info(self, username: str, info_type: str, value: str):
        if info_type == 'diagnosis':
            self.diagnoses = [d for d in self.diagnoses if d != value]
        elif info_type == 'medication':
            self.medications = [m for m in self.medications if m != value]
        elif info_type == 'treatment':
            self.treatments = [t for t in self.treatments if t != value]
        self.save(username)

class Appointment:
    def __init__(self, date: str, time: str, description: str):
        self.date = date
        self.time = time
        self.description = description

    def save(self, username: str):
        with open('appointments.txt', 'a') as f:
            f.write(f"{username}|{self.date}|{self.time}|{self.description}\n")

    @staticmethod
    def load(username: str):
        appointments = []
        with open('appointments.txt', 'r') as f:
            for line in f:
                appointment_data = line.strip().split('|')
                if appointment_data[0] == username:
                    appointments.append(Appointment(appointment_data[1], appointment_data[2], appointment_data[3]))
        return appointments

class App:
    def __init__(self):
        self.users = []
        self.medical_info = None
        self.appointments = []

    def register(self, username: str, password: str):
        if User.username_exists(username):
            return False
        user = User(username, password)
        user.save()
        return True

    def login(self, username: str, password: str) -> bool:
        user = User.load(username)
        if user and user.password == password:
            session['username'] = username
            return True
        return False

    def add_medical_info(self, username: str, info: MedicalInfo):
        info.save(username)

    def set_appointment(self, username: str, appointment: Appointment):
        appointment.save(username)

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if app.login(username, password):
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password. Please try again.', 'error')
    return render_template('login.html')

@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if app.register(username, password):
            return redirect(url_for('login'))
        else:
            flash('Username already exists. Please choose a different one.', 'error')
    return render_template('registration.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    username = session['username']
    medical_info = MedicalInfo.load(username)
    appointments = Appointment.load(username)
    return render_template('dashboard.html', medical_info=medical_info, appointments=appointments)

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app = App()
    app.run(port=9045, debug=False)
