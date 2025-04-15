from flask import Flask, render_template, request, redirect, session
from data_handler import DataHandler
from user import User
from medical_info import MedicalInfo
from appointment import Appointment

app = Flask(__name__)
app.secret_key = 'your_secret_key'

data_handler = DataHandler()

@app.route('/')
def home():
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if data_handler.login(username, password):
            session['username'] = username
            return redirect('/dashboard')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User(username, password)
        if user.save():
            return redirect('/login')
        else:
            return render_template('registration.html', error="Username already exists.")
    return render_template('registration.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect('/login')
    medical_info = data_handler.load_medical_info()
    appointments = data_handler.load_appointments()
    return render_template('dashboard.html', medical_info=medical_info.view_info(), appointments=appointments.view_appointments())

@app.route('/add_medical_info', methods=['GET', 'POST'])
def add_medical_info():
    if 'username' not in session:
        return redirect('/login')
    if request.method == 'POST':
        diagnosis = request.form['diagnosis']
        medication = request.form['medication']
        treatment = request.form['treatment']
        medical_info = data_handler.load_medical_info()
        medical_info.add_diagnosis(diagnosis)
        medical_info.add_medication(medication)
        medical_info.add_treatment(treatment)
        data_handler.save_medical_info(medical_info)
        return redirect('/dashboard')
    return render_template('add_medical_info.html')

@app.route('/add_appointment', methods=['GET', 'POST'])
def add_appointment():
    if 'username' not in session:
        return redirect('/login')
    if request.method == 'POST':
        date = request.form['date']
        time = request.form['time']
        description = request.form['description']
        appointments = data_handler.load_appointments()
        appointments.add_appointment(date, time, description)
        data_handler.save_appointments(appointments)
        return redirect('/dashboard')
    return render_template('add_appointment.html')

if __name__ == '__main__':
    app.run(port=8303, debug=False)
