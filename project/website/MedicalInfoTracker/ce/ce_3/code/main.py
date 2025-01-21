from flask import Flask, render_template, request, redirect, session
from user import User
from medical_info import MedicalInfo
from appointment import Appointment

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Initialize global instances
user_manager = User()
medical_info_manager = MedicalInfo()
appointment_manager = Appointment()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_manager.register(username, password)
        return redirect('/')
    return render_template('register.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'username' not in session:
        return redirect('/')
    
    if request.method == 'POST':
        diagnosis = request.form['diagnosis']
        medication = request.form['medication']
        treatment = request.form['treatment']
        medical_info_manager.add_record(diagnosis, medication, treatment)

    records = medical_info_manager.view_records()
    return render_template('dashboard.html', records=records)

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    if user_manager.login(username, password):
        session['username'] = username
        return redirect('/dashboard')
    return redirect('/')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(port=9043, debug=False)
