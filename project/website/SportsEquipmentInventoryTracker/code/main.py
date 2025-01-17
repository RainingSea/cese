from flask import Flask, render_template, request, redirect, session, url_for
from user_manager import UserManager
from equipment_manager import EquipmentManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure key

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
            return redirect(url_for('login'))
        else:
            return render_template('registration.html', error="Username already exists.")
    return render_template('registration.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        if 'search' in request.form:
            query = request.form['search']
            equipment_list = equipment_manager.search_equipment(query)
        else:
            name = request.form['name']
            quantity = request.form['quantity']
            condition = request.form['condition']
            location = request.form['location']
            equipment_manager.add_equipment(name, int(quantity), condition, location)
            return redirect(url_for('dashboard'))

    equipment_list = equipment_manager.load_equipment()
    return render_template('dashboard.html', equipment_list=equipment_list)

@app.route('/login', methods=['POST'])
def user_login():
    username = request.form['username']
    password = request.form['password']
    if user_manager.login(username, password):
        session['username'] = username
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/logout')
def user_logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/update_equipment/<int:index>', methods=['GET', 'POST'])
def update_equipment(index):
    if 'username' not in session:
        return redirect(url_for('login'))

    equipment_list = equipment_manager.load_equipment()
    if request.method == 'POST':
        name = request.form['name']
        quantity = request.form['quantity']
        condition = request.form['condition']
        location = request.form['location']
        equipment_manager.update_equipment(index, name, int(quantity), condition, location)
        return redirect(url_for('dashboard'))

    equipment = equipment_list[index]
    return render_template('update_equipment.html', equipment=equipment, index=index)

@app.route('/set_alert/<int:index>', methods=['GET', 'POST'])
def set_alert(index):
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        alert_message = request.form['alert_message']
        equipment_manager.set_alert(index, alert_message)
        return redirect(url_for('dashboard'))

    equipment = equipment_manager.load_equipment()[index]
    return render_template('set_alert.html', equipment=equipment, index=index)

@app.route('/view_equipment/<int:index>', methods=['GET'])
def view_equipment(index):
    if 'username' not in session:
        return redirect(url_for('login'))

    equipment = equipment_manager.load_equipment()[index]
    return render_template('view_equipment.html', equipment=equipment)

if __name__ == '__main__':
    app.run(port=8763, debug=False)
