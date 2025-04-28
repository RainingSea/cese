from flask import Flask, render_template, request, redirect, url_for, session
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class UserManager:
    def __init__(self):
        self.users = self.load_users()

    def load_users(self):
        users = {}
        try:
            with open('users.txt', 'r') as file:
                for line in file:
                    username, password = line.strip().split('|')
                    users[username] = password
        except FileNotFoundError:
            pass
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
        medical_info = {}
        try:
            with open('medical_info.txt', 'r') as file:
                for line in file:
                    username, info = line.strip().split('|')
                    medical_info[username] = json.loads(info)
        except FileNotFoundError:
            pass
        return medical_info

    def add_medical_info(self, user: str, info: dict) -> bool:
        self.medical_info[user] = info
        with open('medical_info.txt', 'a') as file:
            file.write(f"{user}|{json.dumps(info)}\n")
        return True

    def get_medical_info(self, user: str) -> dict:
        return self.medical_info.get(user, {})

class AppointmentManager:
    def __init__(self):
        self.appointments = self.load_appointments()

    def load_appointments(self):
        appointments = {}
        try:
            with open('appointments.txt', 'r') as file:
                for line in file:
                    username, appointment = line.strip().split('|')
                    if username not in appointments:
                        appointments[username] = []
                    appointments[username].append(appointment)
        except FileNotFoundError:
            pass
        return appointments

    def set_appointment(self, user: str, appointment: dict) -> bool:
        if user not in self.appointments:
            self.appointments[user] = []
        self.appointments[user].append(appointment)
        with open('appointments.txt', 'a') as file:
            file.write(f"{user}|{json.dumps(appointment)}\n")
        return True

    def get_appointments(self, user: str) -> list:
        return self.appointments.get(user, [])

@app.route('/', methods=['GET', 'POST'])
def login():
    user_manager = UserManager()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.login(username, password):
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            return "Invalid credentials", 401
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    user_manager = UserManager()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            return redirect(url_for('login'))
        else:
            return "Username already exists", 400
    return render_template('registration.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html', username=session['username'])

if __name__ == '__main__':
    app.run(port=8342, debug=False)
