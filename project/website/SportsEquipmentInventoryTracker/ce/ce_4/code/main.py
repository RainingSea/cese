from flask import Flask, render_template, request, redirect, url_for, session
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
    return render_template('register.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if request.method == 'POST':
        if 'logout' in request.form:
            session.pop('username', None)
            return redirect(url_for('login'))
    equipment_list = equipment_manager.load_equipment()
    return render_template('dashboard.html', equipment=equipment_list)

if __name__ == '__main__':
    app.run(port=8651, debug=False)
