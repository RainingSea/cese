from flask import Flask, render_template, request, redirect, session
from user import User
from medical_info import MedicalInfo
from appointment import Appointment

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/')
def home():
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User(username, password)
        if user.authenticate():
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
            return render_template('registration.html', error='Username already exists.')
    return render_template('registration.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect('/login')
    medical_info = MedicalInfo()
    medical_info.load()
    appointments = Appointment()
    appointments.load()
    return render_template('dashboard.html', medical_info=medical_info, appointments=appointments)

@app.route('/add_medical_info', methods=['POST'])
def add_medical_info():
    if 'username' not in session:
        return redirect('/login')
    diagnosis = request.form['diagnosis']
    medication = request.form['medication']
    treatment = request.form['treatment']
    
    medical_info = MedicalInfo()
    medical_info.load()
    if diagnosis:
        medical_info.add_diagnosis(diagnosis)
    if medication:
        medical_info.add_medication(medication)
    if treatment:
        medical_info.add_treatment(treatment)
    
    return redirect('/dashboard')

@app.route('/add_appointment', methods=['POST'])
def add_appointment():
    if 'username' not in session:
        return redirect('/login')
    date = request.form['date']
    time = request.form['time']
    description = request.form['description']
    
    appointment = Appointment()
    appointment.load()
    appointment.add_appointment(date, time, description)
    
    return redirect('/dashboard')

if __name__ == '__main__':
    app.run(port=8302, debug=False)
