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

def load_medical_info():
    medical_info = {}
    with open('medical_info.txt', 'r') as file:
        for line in file:
            username, info = line.strip().split('|')
            medical_info[username] = info.split(',')
    return medical_info

def load_appointments():
    appointments = {}
    with open('appointments.txt', 'r') as file:
        for line in file:
            username, appointment = line.strip().split('|')
            if username not in appointments:
                appointments[username] = []
            appointments[username].append(appointment)
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
    return render_template('register.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        diagnoses = request.form.getlist('diagnoses')
        medications = request.form.getlist('medications')
        treatments = request.form.getlist('treatments')
        medical_info = MedicalInfo(diagnoses, medications, treatments)
        medical_info.save()
        
        date = request.form['date']
        time = request.form['time']
        description = request.form['description']
        appointment = Appointment(date, time, description)
        appointment.save()
        
    return render_template('dashboard.html', username=session['username'])

@app.route('/login', methods=['POST'])
def do_login():
    users = load_users()
    username = request.form['username']
    password = request.form['password']
    if username in users and users[username] == password:
        session['username'] = username
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8639, debug=False)
