from flask import Flask, render_template, request, redirect, session
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class UserManager:
    def __init__(self):
        self.users = self.load_users()

    def load_users(self):
        if os.path.exists('users.txt'):
            with open('users.txt', 'r') as f:
                return [line.strip().split('|') for line in f.readlines()]
        return []

    def register(self, username: str, password: str) -> bool:
        for user in self.users:
            if user[0] == username:
                return False  # User already exists
        self.users.append([username, password])
        with open('users.txt', 'a') as f:
            f.write(f"{username}|{password}\n")
        return True

    def login(self, username: str, password: str) -> bool:
        for user in self.users:
            if user[0] == username and user[1] == password:
                return True
        return False

class MedicalInfoManager:
    def __init__(self):
        self.medical_info = self.load_medical_info()

    def load_medical_info(self):
        if os.path.exists('medical_info.txt'):
            with open('medical_info.txt', 'r') as f:
                return [line.strip() for line in f.readlines()]
        return []

    def add_medical_info(self, info: str) -> None:
        self.medical_info.append(info)
        with open('medical_info.txt', 'a') as f:
            f.write(f"{info}\n")

    def edit_medical_info(self, info_id: int, new_info: str) -> None:
        if 0 <= info_id < len(self.medical_info):
            self.medical_info[info_id] = new_info
            with open('medical_info.txt', 'w') as f:
                f.write('\n'.join(self.medical_info) + '\n')

    def view_medical_info(self):
        return self.medical_info

class AppointmentManager:
    def __init__(self):
        self.appointments = self.load_appointments()

    def load_appointments(self):
        if os.path.exists('appointments.txt'):
            with open('appointments.txt', 'r') as f:
                return [line.strip() for line in f.readlines()]
        return []

    def set_reminder(self, date: str, time: str) -> None:
        reminder = f"{date} {time}"
        self.appointments.append(reminder)
        with open('appointments.txt', 'a') as f:
            f.write(f"{reminder}\n")

    def view_reminders(self):
        return self.appointments

user_manager = UserManager()
medical_info_manager = MedicalInfoManager()
appointment_manager = AppointmentManager()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            return redirect('/')
        else:
            return "User already exists."
    return render_template('registration.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if request.method == 'POST':
        if 'logout' in request.form:
            session.pop('username', None)
            return redirect('/')
        elif 'add_medical_info' in request.form:
            info = request.form['medical_info']
            medical_info_manager.add_medical_info(info)
        elif 'set_reminder' in request.form:
            date = request.form['date']
            time = request.form['time']
            appointment_manager.set_reminder(date, time)
    return render_template('dashboard.html', 
                           medical_info=medical_info_manager.view_medical_info(), 
                           reminders=appointment_manager.view_reminders())

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    if user_manager.login(username, password):
        session['username'] = username
        return redirect('/dashboard')
    return "Invalid credentials."

if __name__ == '__main__':
    app.run(port=8180, debug=False)
