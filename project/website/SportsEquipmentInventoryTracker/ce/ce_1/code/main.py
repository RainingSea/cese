from flask import Flask, render_template, request, redirect, session, url_for
from user import User
from equipment import Equipment
from alert import Alert

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Load users from the text file
def load_users():
    user_instance = User("", "")
    return user_instance.load_users()

# Load equipment from the text file
def load_equipment():
    equipment_instance = Equipment("", "", 0, "", True, "")
    return equipment_instance.load_equipment()

# Load alerts from the text file
def load_alerts():
    alert_instance = Alert("", "")
    return alert_instance.load_alerts()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User(username, password)
        user.save()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    equipment_data = load_equipment()
    alerts_data = load_alerts()
    
    if request.method == 'POST':
        if 'add_equipment' in request.form:
            name = request.form['name']
            type_ = request.form['type']
            quantity = int(request.form['quantity'])
            condition = request.form['condition']
            availability = request.form['availability'] == 'true'
            location = request.form['location']
            equipment = Equipment(name, type_, quantity, condition, availability, location)
            equipment.save()
            return redirect(url_for('dashboard'))

    return render_template('dashboard.html', equipment=equipment_data, alerts=alerts_data)

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    
    users = load_users()
    for user in users:
        if user.username == username and user.password == password:
            session['username'] = username
            return redirect(url_for('dashboard'))
    
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8648, debug=False)
