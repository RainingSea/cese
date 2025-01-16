from flask import Flask, render_template, request, redirect, url_for, flash, session
from user_manager import UserManager
from equipment_manager import EquipmentManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'

user_manager = UserManager('users.txt')
equipment_manager = EquipmentManager('equipment.txt')

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            flash('Registration successful! Please log in.')
            return redirect(url_for('login'))
        else:
            flash('Username already exists. Please choose another one.')
    return render_template('registration.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        if 'login' in request.form:
            username = request.form['username']
            password = request.form['password']
            if user_manager.login(username, password):
                session['username'] = username
                return render_template('dashboard.html', equipment=equipment_manager.get_equipment())
            else:
                flash('Invalid username or password.')
        elif 'add_equipment' in request.form:
            name = request.form['name']
            quantity = int(request.form['quantity'])
            condition = request.form['condition']
            location = request.form['location']
            equipment_manager.add_equipment(name, quantity, condition, location)

    search_query = request.args.get('search', '')
    filter_condition = request.args.get('condition', '')
    equipment = equipment_manager.search_equipment(search_query) if search_query else equipment_manager.filter_equipment(filter_condition, True) if filter_condition else equipment_manager.get_equipment()

    return render_template('dashboard.html', equipment=equipment)

@app.route('/logout')
def logout():
    session.clear()  # Clear the entire session
    return redirect(url_for('login'))

@app.route('/update_equipment', methods=['POST'])
def update_equipment():
    if 'username' not in session:
        return redirect(url_for('login'))

    name = request.form['name']
    quantity = int(request.form['quantity'])
    condition = request.form['condition']
    location = request.form['location']
    equipment_manager.update_equipment(name, quantity, condition, location)
    flash('Equipment updated successfully!')
    return redirect(url_for('dashboard'))

@app.route('/set_alert', methods=['POST'])
def set_alert():
    if 'username' not in session:
        return redirect(url_for('login'))

    equipment_name = request.form['equipment_name']
    alert_message = request.form['alert_message']
    equipment_manager.set_alert(equipment_name, alert_message)
    flash('Alert set successfully!')
    return redirect(url_for('dashboard'))

@app.route('/equipment/<name>', methods=['GET'])
def view_equipment_details(name):
    if 'username' not in session:
        return redirect(url_for('login'))

    equipment_item = equipment_manager.get_equipment_details(name)
    if equipment_item:
        return render_template('equipment_details.html', equipment=equipment_item)
    else:
        flash('Equipment not found.')
        return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(port=8652, debug=False)
