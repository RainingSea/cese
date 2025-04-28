from flask import Flask, render_template, request, redirect, url_for
from UserManager import UserManager
from EquipmentManager import EquipmentManager

app = Flask(__name__)
user_manager = UserManager()
equipment_manager = EquipmentManager()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.login(username, password):
            return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_manager.register(username, password)
        return redirect(url_for('login'))
    return render_template('registration.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if request.method == 'POST':
        name = request.form['name']
        quantity = int(request.form['quantity'])
        condition = request.form['condition']
        location = request.form['location']
        equipment_manager.add_equipment(name, quantity, condition, location)
    equipment_list = equipment_manager.view_equipment()
    return render_template('dashboard.html', equipment_list=equipment_list)

if __name__ == '__main__':
    app.run(port=8424, debug=False)
