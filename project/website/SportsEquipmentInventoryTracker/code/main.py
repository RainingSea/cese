from flask import Flask, render_template, request, redirect, url_for, flash, session
from tools import load_users, save_users, load_equipment, save_equipment
from user_manager import UserManager
from equipment_manager import EquipmentManager

app = Flask(__name__)
app.secret_key = 'supersecretkey'

user_manager = UserManager()
equipment_manager = EquipmentManager()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        login_result = user_manager.login(username, password)
        if login_result['success']:
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            flash(login_result['message'])
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        registration_result = user_manager.register(username, password)
        flash(registration_result['message'])
        if registration_result['success']:
            return redirect(url_for('login'))
    return render_template('registration.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        search_query = request.form.get('search_query')
        if search_query:
            equipment = equipment_manager.search_equipment(search_query)
        else:
            equipment = equipment_manager.equipment
    else:
        equipment = equipment_manager.equipment

    return render_template('dashboard.html', equipment=equipment)

@app.route('/add_equipment', methods=['GET', 'POST'])
def add_equipment():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        name = request.form['name']
        type_ = request.form['type']
        quantity = request.form['quantity']
        condition = request.form['condition']
        location = request.form['location']
        equipment_manager.add_equipment(name, type_, int(quantity), condition, location)
        flash('Equipment added successfully.')
        return redirect(url_for('dashboard'))
    return render_template('add_equipment.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out.')
    return redirect(url_for('login'))

if __name__ == '__main__':
    user_manager.load_users()
    equipment_manager.load_equipment()
    app.run(port=8253, debug=False)
