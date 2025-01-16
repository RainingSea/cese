from flask import Flask, render_template, request, redirect, session, url_for
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
            return redirect(url_for('login'))
        else:
            return "Username already exists!"
    return render_template('register.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        name = request.form['name']
        quantity = int(request.form['quantity'])
        condition = request.form['condition']
        location = request.form['location']
        equipment_manager.add_equipment(name, quantity, condition, location)
    equipment_list = equipment_manager.equipment
    return render_template('dashboard.html', equipment_list=equipment_list)

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    if user_manager.login(username, password):
        session['username'] = username
        return redirect(url_for('dashboard'))
    return "Invalid username or password!"

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8647, debug=False)
