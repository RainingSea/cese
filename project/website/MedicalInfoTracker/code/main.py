from flask import Flask, render_template, request, redirect, url_for, session, flash
from user_manager import UserManager
from medical_info_manager import MedicalInfoManager
from appointment_manager import AppointmentManager
from reminder_manager import ReminderManager

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

user_manager = UserManager('users.txt')
medical_info_manager = MedicalInfoManager('medical_info.txt')
appointment_manager = AppointmentManager('appointments.txt')
reminder_manager = ReminderManager('reminders.txt')

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
        flash('Username already exists. Please choose a different one.', 'error')
    return render_template('registration.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        info = request.form['medical_info']
        medical_info_manager.add_medical_info(session['username'], info)

    medical_info = medical_info_manager.get_medical_info(session['username'])
    appointments = appointment_manager.get_appointments(session['username'])
    return render_template('dashboard.html', medical_info=medical_info, appointments=appointments)

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    if user_manager.login(username, password):
        session['username'] = username
        return redirect(url_for('dashboard'))
    flash('Invalid username or password. Please try again.', 'error')
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

@app.route('/set_appointment', methods=['POST'])
def set_appointment():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    appointment = request.form['appointment']
    appointment_manager.set_appointment(session['username'], appointment)
    return redirect(url_for('dashboard'))

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
    app.run(port=8345, debug=False)
