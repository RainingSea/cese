from flask import Flask, render_template, request, redirect, session, url_for
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class User:
    def __init__(self):
        self.username = ""
        self.password = ""

    def register(self, username: str, password: str) -> bool:
        with open('users.txt', 'a') as f:
            f.write(f"{username}|{password}\n")
        return True

    def login(self, username: str, password: str) -> bool:
        with open('users.txt', 'r') as f:
            for line in f:
                user, pwd = line.strip().split('|')
                if user == username and pwd == password:
                    return True
        return False

class MedicalInfo:
    def __init__(self):
        self.diagnoses = []
        self.medications = []
        self.treatments = []

    def add_entry(self, diagnosis: str, medication: str, treatment: str) -> None:
        self.diagnoses.append(diagnosis)
        self.medications.append(medication)
        self.treatments.append(treatment)
        with open('medical_info.txt', 'a') as f:
            f.write(f"{diagnosis}|{medication}|{treatment}\n")

    def get_history(self) -> dict:
        history = []
        with open('medical_info.txt', 'r') as f:
            for line in f:
                history.append(line.strip().split('|'))
        return {"history": history}

class Appointment:
    def __init__(self):
        self.appointments = []

    def set_reminder(self, date: str, time: str, description: str) -> None:
        self.appointments.append({"date": date, "time": time, "description": description})
        with open('appointments.txt', 'a') as f:
            f.write(f"{date}|{time}|{description}\n")

    def get_reminders(self) -> list:
        reminders = []
        with open('appointments.txt', 'r') as f:
            for line in f:
                reminders.append(line.strip().split('|'))
        return reminders

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User()
        if user.login(username, password):
            session['username'] = username
            return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User()
        user.register(username, password)
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    medical_info = MedicalInfo()
    appointment = Appointment()
    history = medical_info.get_history()
    reminders = appointment.get_reminders()
    return render_template('dashboard.html', history=history, reminders=reminders)

if __name__ == '__main__':
    app.run(port=9044, debug=False)
