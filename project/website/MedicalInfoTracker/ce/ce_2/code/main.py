from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

class UserManager:
    def __init__(self):
        self.users = self.load_users()

    def load_users(self):
        users = {}
        with open('users.txt', 'r') as file:
            for line in file:
                username, password = line.strip().split('|')
                users[username] = password
        return users

    def register(self, username: str, password: str) -> bool:
        if username in self.users:
            return False
        self.users[username] = password
        with open('users.txt', 'a') as file:
            file.write(f"{username}|{password}\n")
        return True

    def login(self, username: str, password: str) -> bool:
        return self.users.get(username) == password

class MedicalInfoManager:
    def __init__(self):
        self.medical_info = self.load_medical_info()

    def load_medical_info(self):
        medical_info = []
        with open('medical_info.txt', 'r') as file:
            for line in file:
                medical_info.append(line.strip().split('|'))
        return medical_info

    def add_info(self, diagnosis: str, medication: str, treatment: str) -> None:
        self.medical_info.append([diagnosis, medication, treatment])
        with open('medical_info.txt', 'a') as file:
            file.write(f"{diagnosis}|{medication}|{treatment}\n")

    def view_info(self) -> list:
        return self.medical_info

class ReminderManager:
    def __init__(self):
        self.reminders = self.load_reminders()

    def load_reminders(self):
        reminders = []
        with open('reminders.txt', 'r') as file:
            for line in file:
                reminders.append(line.strip().split('|'))
        return reminders

    def set_reminder(self, date: str, time: str, description: str) -> None:
        self.reminders.append([date, time, description])
        with open('reminders.txt', 'a') as file:
            file.write(f"{date}|{time}|{description}\n")

    def get_reminders(self) -> list:
        return self.reminders

app = Flask(__name__)
user_manager = UserManager()
medical_info_manager = MedicalInfoManager()
reminder_manager = ReminderManager()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.login(username, password):
            return redirect(url_for('medical_info'))
        else:
            return "Invalid credentials"
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            return redirect(url_for('login'))
        else:
            return "Username already exists"
    return render_template('registration.html')

@app.route('/medical_info', methods=['GET', 'POST'])
def medical_info():
    if request.method == 'POST':
        diagnosis = request.form['diagnosis']
        medication = request.form['medication']
        treatment = request.form['treatment']
        medical_info_manager.add_info(diagnosis, medication, treatment)
    info = medical_info_manager.view_info()
    return render_template('medical_info.html', info=info)

@app.route('/reminders', methods=['GET', 'POST'])
def reminders():
    if request.method == 'POST':
        date = request.form['date']
        time = request.form['time']
        description = request.form['description']
        reminder_manager.set_reminder(date, time, description)
    reminders = reminder_manager.get_reminders()
    return render_template('reminders.html', reminders=reminders)

if __name__ == '__main__':
    app.run(port=8344, debug=False)
