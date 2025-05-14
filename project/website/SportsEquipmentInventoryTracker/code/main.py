from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

class AuthManager:
    def __init__(self):
        self.users_file = 'users.txt'
    
    def login(self, username, password):
        try:
            with open(self.users_file, 'r') as f:
                for line in f:
                    stored_username, stored_password = line.strip().split('|')
                    if stored_username == username and stored_password == password:
                        session['username'] = username
                        session['_fresh'] = True
                        return True
        except FileNotFoundError:
            with open(self.users_file, 'w') as f:
                pass
        return False
    
    def register(self, username, password):
        try:
            with open(self.users_file, 'a+') as f:
                f.seek(0)
                for line in f:
                    if line.split('|')[0] == username:
                        return False
                f.write(f"{username}|{password}\n")
                f.flush()
                return True
        except:
            return False

    def logout(self):
        session.clear()
        return True

class EquipmentTracker:
    def __init__(self):
        self.equipment_file = 'equipment.txt'
    
    def get_all(self):
        equipment = []
        try:
            with open(self.equipment_file, 'r') as f:
                for line in f:
                    parts = line.strip().split('|')
                    if len(parts) >= 8:
                        equipment.append({
                            'id': parts[0],
                            'name': parts[1],
                            'type': parts[2],
                            'quantity': parts[3],
                            'condition': parts[4],
                            'availability': parts[5],
                            'location': parts[6],
                            'alert_date': parts[7]
                        })
        except FileNotFoundError:
            with open(self.equipment_file, 'w') as f:
                pass
        return equipment
    
    def search_equipment(self, query, filter_type=None):
        results = []
        try:
            with open(self.equipment_file, 'r') as f:
                for line in f:
                    parts = line.strip().split('|')
                    if len(parts) >= 8:
                        matches_filter = filter_type is None or parts[2].lower() == filter_type.lower()
                        matches_query = query.lower() in parts[1].lower()
                        if matches_filter and matches_query:
                            results.append({
                                'id': parts[0],
                                'name': parts[1],
                                'type': parts[2],
                                'quantity': parts[3],
                                'condition': parts[4],
                                'availability': parts[5],
                                'location': parts[6],
                                'alert_date': parts[7]
                            })
        except FileNotFoundError:
            pass
        return results
    
    def add_equipment(self, data):
        try:
            if not self._validate_date(data['alert_date']):
                return False
            with open(self.equipment_file, 'a+') as f:
                f.seek(0)
                lines = f.readlines()
                new_id = str(len(lines) + 1)
                equipment_data = f"{new_id}|{data['name']}|{data['type']}|{data['quantity']}|{data['condition']}|{data['availability']}|{data['location']}|{data['alert_date']}\n"
                f.write(equipment_data)
                f.flush()
                return True
        except:
            return False
    
    def update_equipment(self, id, updates):
        try:
            if 'alert_date' in updates and not self._validate_date(updates['alert_date']):
                return False
            with open(self.equipment_file, 'r') as f:
                lines = f.readlines()
            
            with open(self.equipment_file, 'w') as f:
                for line in lines:
                    parts = line.strip().split('|')
                    if parts[0] == id and len(parts) >= 8:
                        for key, value in updates.items():
                            if key == 'name':
                                parts[1] = value
                            elif key == 'type':
                                parts[2] = value
                            elif key == 'quantity':
                                parts[3] = value
                            elif key == 'condition':
                                parts[4] = value
                            elif key == 'availability':
                                parts[5] = value
                            elif key == 'location':
                                parts[6] = value
                            elif key == 'alert_date':
                                parts[7] = value
                        line = '|'.join(parts) + '\n'
                    f.write(line)
                f.flush()
            return True
        except:
            return False
    
    def _validate_date(self, date_str):
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
            return True
        except ValueError:
            return False

class AlertSystem:
    def __init__(self):
        self.alerts_file = 'alerts.txt'
    
    def check_alerts(self):
        alerts = []
        try:
            with open(self.alerts_file, 'r') as f:
                for line in f:
                    parts = line.strip().split('|')
                    if len(parts) >= 3:
                        alerts.append({
                            'equipment_id': parts[0],
                            'alert_type': parts[1],
                            'threshold_date': parts[2]
                        })
        except FileNotFoundError:
            with open(self.alerts_file, 'w') as f:
                pass
        return alerts
    
    def create_alert(self, equipment_id, alert_data):
        try:
            if not self._validate_date(alert_data['threshold_date']):
                return False
            with open(self.alerts_file, 'a+') as f:
                f.write(f"{equipment_id}|{alert_data['alert_type']}|{alert_data['threshold_date']}\n")
                f.flush()
            return True
        except:
            return False
    
    def _validate_date(self, date_str):
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
            return True
        except ValueError:
            return False

auth_manager = AuthManager()
equipment_tracker = EquipmentTracker()
alert_system = AlertSystem()

@app.route('/')
def home():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if auth_manager.login(username, password):
            return redirect(url_for('dashboard'))
        flash('Invalid credentials', 'error')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if auth_manager.register(username, password):
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        flash('Username already exists', 'error')
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    equipment = equipment_tracker.get_all()
    alerts = alert_system.check_alerts()
    return render_template('dashboard.html', equipment=equipment, alerts=alerts)

@app.route('/search_equipment', methods=['POST'])
def search_equipment():
    if 'username' not in session:
        return redirect(url_for('login'))
    query = request.form['query']
    filter_type = request.form.get('filter_type')
    results = equipment_tracker.search_equipment(query, filter_type)
    return render_template('dashboard.html', equipment=results, alerts=alert_system.check_alerts())

@app.route('/add_equipment', methods=['POST'])
def add_equipment():
    if 'username' not in session:
        return redirect(url_for('login'))
    data = {
        'name': request.form['name'],
        'type': request.form['type'],
        'quantity': request.form['quantity'],
        'condition': request.form['condition'],
        'availability': request.form['availability'],
        'location': request.form['location'],
        'alert_date': request.form['alert_date']
    }
    if equipment_tracker.add_equipment(data):
        flash('Equipment added successfully', 'success')
    else:
        flash('Failed to add equipment. Check date format (YYYY-MM-DD).', 'error')
    return redirect(url_for('dashboard'))

@app.route('/update_equipment/<id>', methods=['POST'])
def update_equipment(id):
    if 'username' not in session:
        return redirect(url_for('login'))
    updates = {
        'name': request.form['name'],
        'type': request.form['type'],
        'quantity': request.form['quantity'],
        'condition': request.form['condition'],
        'availability': request.form['availability'],
        'location': request.form['location'],
        'alert_date': request.form['alert_date']
    }
    if equipment_tracker.update_equipment(id, updates):
        flash('Equipment updated successfully', 'success')
    else:
        flash('Failed to update equipment. Check date format (YYYY-MM-DD).', 'error')
    return redirect(url_for('dashboard'))

@app.route('/add_alert', methods=['POST'])
def add_alert():
    if 'username' not in session:
        return redirect(url_for('login'))
    alert_data = {
        'alert_type': request.form['alert_type'],
        'threshold_date': request.form['threshold_date']
    }
    if alert_system.create_alert(request.form['equipment_id'], alert_data):
        flash('Alert added successfully', 'success')
    else:
        flash('Failed to add alert. Check date format (YYYY-MM-DD).', 'error')
    return redirect(url_for('dashboard'))

@app.route('/alerts')
def alerts():
    if 'username' not in session:
        return redirect(url_for('login'))
    alerts = alert_system.check_alerts()
    equipment = equipment_tracker.get_all()
    return render_template('alerts.html', alerts=alerts, equipment=equipment)

@app.route('/logout')
def logout():
    auth_manager.logout()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8116, debug=False)
