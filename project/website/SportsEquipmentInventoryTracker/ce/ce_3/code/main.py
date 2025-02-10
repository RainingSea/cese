from flask import Flask, render_template, request, redirect, url_for, session
from user import User
from equipment import Equipment
from auth import Auth
from dashboard import Dashboard

app = Flask(__name__)
app.secret_key = 'your_secret_key'

auth = Auth()
dashboard = Dashboard()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if auth.register(username, password):
            return redirect(url_for('login'))
    return render_template('registration.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard_view():
    if request.method == 'POST':
        name = request.form['name']
        type_ = request.form['type']
        quantity = int(request.form['quantity'])
        condition = request.form['condition']
        availability = request.form.get('availability') == 'on'
        location = request.form['location']
        maintenance_alert = request.form['maintenance_alert']
        equipment = Equipment(name, type_, quantity, condition, availability, location, maintenance_alert)
        dashboard.add_equipment(equipment)
    equipment_list = dashboard.load_equipment()
    return render_template('dashboard.html', equipment_list=equipment_list)

@app.route('/login', methods=['POST'])
def login_user():
    username = request.form['username']
    password = request.form['password']
    if auth.login(username, password):
        session['username'] = username
        return redirect(url_for('dashboard_view'))
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8650, debug=False)
