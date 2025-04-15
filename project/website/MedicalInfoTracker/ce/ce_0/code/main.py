from flask import Flask, render_template, request, redirect, session
from data_handler import DataHandler
from user import User
from medical_info import MedicalInfo
from appointment import Appointment

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a more secure key

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
    return render_template('dashboard.html')

@app.route('/medical_info', methods=['GET', 'POST'])
def medical_info():
    medical_info = data_handler.load_medical_info()
    if request.method == 'POST':
        if 'diagnosis' in request.form:
            medical_info.add_diagnosis(request.form['diagnosis'])
        elif 'medication' in request.form:
            medical_info.add_medication(request.form['medication'])
        elif 'treatment' in request.form:
            medical_info.add_treatment(request.form['treatment'])
        data_handler.save_medical_info(medical_info)
    return render_template('medical_info.html', medical_info=medical_info)

@app.route('/appointments', methods=['GET', 'POST'])
def appointments():
    appointment_manager = data_handler.load_appointments()
    if request.method == 'POST':
        date = request.form['date']
        time = request.form['time']
        description = request.form['description']
        appointment_manager.add_appointment(date, time, description)
        data_handler.save_appointments(appointment_manager)
    return render_template('appointments.html', appointments=appointment_manager.appointments)

if __name__ == '__main__':
    app.run(port=8301, debug=False)
