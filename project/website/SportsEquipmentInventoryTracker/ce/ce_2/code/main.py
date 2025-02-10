from flask import Flask, render_template, request, redirect, url_for, session
from user_manager import UserManager
from equipment_manager import EquipmentManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'

user_manager = UserManager()
equipment_manager = EquipmentManager()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.add_user(username, password):
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        if 'add_equipment' in request.form:
            name = request.form['name']
            type_ = request.form['type']
            quantity = int(request.form['quantity'])
            condition = request.form['condition']
            location = request.form['location']
            equipment_manager.add_equipment(name, type_, quantity, condition, location)
    
    equipment_list = equipment_manager.load_equipment()
    return render_template('dashboard.html', equipment=equipment_list)

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    if user_manager.authenticate(username, password):
        session['username'] = username
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    user_manager.load_users()
    equipment_manager.load_equipment()
    app.run(port=8649, debug=False)
