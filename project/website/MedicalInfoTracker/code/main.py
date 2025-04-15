from flask import Flask, render_template, request, redirect, url_for, session
from user import User
from medical_info import MedicalInfo
from appointment import Appointment
from data_handler import DataHandler

app = Flask(__name__)
app.secret_key = 'your_secret_key'

data_handler = DataHandler()

@app.route('/')
def login_page():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    if User.login(username, password):
        session['username'] = username
        return redirect(url_for('dashboard'))
    return redirect(url_for('login_page'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User(username, password)
        if user.save():
            return redirect(url_for('login_page'))
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login_page'))
    medical_info = data_handler.load_medical_info()
    appointments = data_handler.load_appointments()
    return render_template('dashboard.html', medical_info=medical_info.view_history(), appointments=appointments)

@app.route('/logout')
def logout():
    session.clear()  # Clear the session
    return redirect('/')

@app.route('/add_medical_info', methods=['POST'])
def add_medical_info():
    if 'username' not in session:
        return redirect('/login')
    diagnosis = request.form.get('diagnosis')
    medication = request.form.get('medication')
    treatment = request.form.get('treatment')
    
    medical_info = data_handler.load_medical_info()
    if diagnosis:
        medical_info.add_diagnosis(diagnosis)
    if medication:
        medical_info.add_medication(medication)
    if treatment:
        medical_info.add_treatment(treatment)
    
    data_handler.save_medical_info(medical_info)
    return redirect('/dashboard')

@app.route('/add_appointment', methods=['POST'])
def add_appointment():
    if 'username' not in session:
        return redirect('/login')
    date = request.form.get('date')
    time = request.form.get('time')
    description = request.form.get('description')
    
    appointments = data_handler.load_appointments()
    if not any(appointment.date == date and appointment.time == time for appointment in appointments):
        appointment = Appointment(date, time, description)
        data_handler.save_appointment(appointment)
    
    return redirect('/dashboard')

if __name__ == '__main__':
    app.run(port=8304, debug=False)
