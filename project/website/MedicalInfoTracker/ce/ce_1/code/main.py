from flask import Flask, render_template, request, redirect, url_for, session
from user_manager import UserManager
from medical_info_manager import MedicalInfoManager
from appointment_manager import AppointmentManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this in production

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
            return redirect(url_for('login'))
    return render_template('registration.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        if 'diagnosis' in request.form:
            medical_info_manager.add_diagnosis(request.form['diagnosis'])
        elif 'medication' in request.form:
            medical_info_manager.add_medication(request.form['medication'])
        elif 'treatment' in request.form:
            medical_info_manager.add_treatment(request.form['treatment'])
        elif 'reminder_date' in request.form and 'reminder_time' in request.form:
            appointment_manager.set_reminder(request.form['reminder_date'], request.form['reminder_time'])

    medical_info = medical_info_manager.view_medical_info()
    reminders = appointment_manager.view_reminders()
    return render_template('dashboard.html', medical_info=medical_info, reminders=reminders)

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    if user_manager.login(username, password):
        session['username'] = username
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8343, debug=False)
