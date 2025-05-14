from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

class UserManager:
    def __init__(self, users_file='users.txt'):
        self.users_file = users_file

    def register(self, username, password):
        with open(self.users_file, 'a') as f:
            f.write(f"{username}|{password}\n")
        return True

    def login(self, username, password):
        with open(self.users_file, 'r') as f:
            for line in f:
                stored_username, stored_password = line.strip().split('|')
                if username == stored_username and password == stored_password:
                    return True
        return False

class EquipmentTracker:
    def __init__(self, equipment_file='equipment.txt'):
        self.equipment_file = equipment_file

    def add_equipment(self, item):
        with open(self.equipment_file, 'a') as f:
            f.write(f"{item['name']}|{item['type']}|{item['quantity']}|{item['condition']}|{item['location']}|{item['last_maintenance_date']}\n")
        return True

    def update_equipment(self, item):
        equipment = self.get_equipment()
        updated = False
        for i, eq in enumerate(equipment):
            if eq['name'] == item['name']:
                equipment[i] = item
                updated = True
                break
        
        if updated:
            with open(self.equipment_file, 'w') as f:
                for eq in equipment:
                    f.write(f"{eq['name']}|{eq['type']}|{eq['quantity']}|{eq['condition']}|{eq['location']}|{eq['last_maintenance_date']}\n")
            return True
        return False

    def get_equipment(self):
        equipment = []
        with open(self.equipment_file, 'r') as f:
            for line in f:
                name, type_, quantity, condition, location, last_maintenance = line.strip().split('|')
                equipment.append({
                    'name': name,
                    'type': type_,
                    'quantity': quantity,
                    'condition': condition,
                    'location': location,
                    'last_maintenance_date': last_maintenance
                })
        return equipment

    def search_equipment(self, query):
        equipment = self.get_equipment()
        return [eq for eq in equipment if query.lower() in eq['name'].lower()]

    def filter_equipment(self, criteria):
        equipment = self.get_equipment()
        filtered = []
        for eq in equipment:
            match = True
            for key, value in criteria.items():
                if value and str(eq[key]).lower() != value.lower():
                    match = False
                    break
            if match:
                filtered.append(eq)
        return filtered

class AlertSystem:
    def __init__(self, alerts_file='alerts.txt'):
        self.alerts_file = alerts_file

    def set_alert(self, username, equipment, alert_type, date):
        with open(self.alerts_file, 'a') as f:
            f.write(f"{username}|{equipment}|{alert_type}|{date}\n")
        return True

    def check_alerts(self, username):
        alerts = []
        with open(self.alerts_file, 'r') as f:
            for line in f:
                user, equipment, alert_type, date = line.strip().split('|')
                if user == username:
                    alerts.append({
                        'equipment': equipment,
                        'alert_type': alert_type,
                        'date': date
                    })
        return alerts

user_manager = UserManager()
equipment_tracker = EquipmentTracker()
alert_system = AlertSystem()

@app.route('/')
def home():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            return redirect(url_for('login'))
        return "Registration failed"
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.login(username, password):
            session['username'] = username
            return redirect(url_for('dashboard'))
        return "Login failed"
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    equipment = equipment_tracker.get_equipment()
    alerts = alert_system.check_alerts(session['username'])
    return render_template('dashboard.html', 
                          username=session['username'],
                          equipment=equipment,
                          alerts=alerts)

@app.route('/add_equipment', methods=['POST'])
def add_equipment():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    item = {
        'name': request.form['name'],
        'type': request.form['type'],
        'quantity': request.form['quantity'],
        'condition': request.form['condition'],
        'location': request.form['location'],
        'last_maintenance_date': request.form['last_maintenance_date']
    }
    equipment_tracker.add_equipment(item)
    return redirect(url_for('dashboard'))

@app.route('/search_equipment', methods=['POST'])
def search_equipment():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    query = request.form['query']
    results = equipment_tracker.search_equipment(query)
    return render_template('dashboard.html', 
                          username=session['username'],
                          equipment=results,
                          alerts=alert_system.check_alerts(session['username']))

@app.route('/filter_equipment', methods=['POST'])
def filter_equipment():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    criteria = {
        'type': request.form.get('type'),
        'condition': request.form.get('condition'),
        'location': request.form.get('location')
    }
    results = equipment_tracker.filter_equipment(criteria)
    return render_template('dashboard.html', 
                          username=session['username'],
                          equipment=results,
                          alerts=alert_system.check_alerts(session['username']))

@app.route('/set_alert', methods=['POST'])
def set_alert():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    alert_system.set_alert(
        session['username'],
        request.form['equipment_name'],
        request.form['alert_type'],
        request.form['threshold_date']
    )
    return redirect(url_for('dashboard'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8109, debug=False)
