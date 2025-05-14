from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

class FileStorage:
    @staticmethod
    def read_users():
        users = {}
        try:
            with open('users.txt', 'r') as f:
                for line in f:
                    username, password = line.strip().split(':')
                    users[username] = password
        except FileNotFoundError:
            pass
        return users

    @staticmethod
    def write_user(username, password):
        with open('users.txt', 'a') as f:
            f.write(f"{username}:{password}\n")

    @staticmethod
    def read_equipment():
        equipment = []
        try:
            with open('equipment.txt', 'r') as f:
                for line in f:
                    parts = line.strip().split('|')
                    if len(parts) == 8:
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
            pass
        return equipment

    @staticmethod
    def write_equipment(data):
        with open('equipment.txt', 'a') as f:
            line = '|'.join([
                data['id'],
                data['name'],
                data['type'],
                data['quantity'],
                data['condition'],
                data['availability'],
                data['location'],
                data['alert_date']
            ])
            f.write(line + '\n')

    @staticmethod
    def update_equipment(equipment_list):
        with open('equipment.txt', 'w') as f:
            for item in equipment_list:
                line = '|'.join([
                    item['id'],
                    item['name'],
                    item['type'],
                    item['quantity'],
                    item['condition'],
                    item['availability'],
                    item['location'],
                    item['alert_date']
                ])
                f.write(line + '\n')

    @staticmethod
    def read_alerts():
        alerts = []
        try:
            with open('alerts.txt', 'r') as f:
                for line in f:
                    parts = line.strip().split('|')
                    if len(parts) == 3:
                        alerts.append({
                            'equipment_id': parts[0],
                            'alert_type': parts[1],
                            'threshold': parts[2]
                        })
        except FileNotFoundError:
            pass
        return alerts

    @staticmethod
    def write_alert(data):
        with open('alerts.txt', 'a') as f:
            line = '|'.join([
                data['equipment_id'],
                data['alert_type'],
                data['threshold']
            ])
            f.write(line + '\n')

class AuthController:
    @staticmethod
    def login(username, password):
        users = FileStorage.read_users()
        if username in users and users[username] == password:
            return True
        return False

    @staticmethod
    def register(username, password):
        users = FileStorage.read_users()
        if username in users:
            return False
        FileStorage.write_user(username, password)
        return True

class EquipmentController:
    @staticmethod
    def add_equipment(data):
        equipment = FileStorage.read_equipment()
        data['id'] = str(len(equipment) + 1)
        FileStorage.write_equipment(data)
        return True

    @staticmethod
    def update_equipment(id, data):
        equipment = FileStorage.read_equipment()
        for item in equipment:
            if item['id'] == id:
                item.update(data)
                break
        FileStorage.update_equipment(equipment)
        return True

    @staticmethod
    def search_equipment(query):
        equipment = FileStorage.read_equipment()
        results = []
        for item in equipment:
            if (query.lower() in item['name'].lower() or 
                query.lower() in item['type'].lower() or 
                query.lower() in item['location'].lower()):
                results.append(item)
        return results

    @staticmethod
    def filter_equipment(criteria):
        equipment = FileStorage.read_equipment()
        results = []
        for item in equipment:
            match = True
            for key, value in criteria.items():
                if str(item.get(key, '')).lower() != str(value).lower():
                    match = False
                    break
            if match:
                results.append(item)
        return results

    @staticmethod
    def set_alert(equipment_id, alert_data):
        FileStorage.write_alert({
            'equipment_id': equipment_id,
            'alert_type': alert_data['alert_type'],
            'threshold': alert_data['threshold']
        })
        return True

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
        if AuthController.login(username, password):
            session['username'] = username
            return redirect(url_for('dashboard'))
        return render_template('login.html', error='Invalid credentials')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if AuthController.register(username, password):
            return redirect(url_for('login'))
        return render_template('register.html', error='Username already exists')
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    equipment = FileStorage.read_equipment()
    alerts = FileStorage.read_alerts()
    return render_template('dashboard.html', 
                         username=session['username'],
                         equipment=equipment,
                         alerts=alerts)

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
    EquipmentController.add_equipment(data)
    return redirect(url_for('dashboard'))

@app.route('/update_equipment/<id>', methods=['POST'])
def update_equipment(id):
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
    EquipmentController.update_equipment(id, data)
    return redirect(url_for('dashboard'))

@app.route('/set_alert', methods=['POST'])
def set_alert():
    if 'username' not in session:
        return redirect(url_for('login'))
    alert_data = {
        'alert_type': request.form['alert_type'],
        'threshold': request.form['threshold']
    }
    EquipmentController.set_alert(request.form['equipment_id'], alert_data)
    return redirect(url_for('dashboard'))

@app.route('/search_equipment', methods=['POST'])
def search_equipment():
    if 'username' not in session:
        return redirect(url_for('login'))
    query = request.form['query']
    results = EquipmentController.search_equipment(query)
    return render_template('dashboard.html', 
                         username=session['username'],
                         equipment=results,
                         alerts=FileStorage.read_alerts())

@app.route('/filter_equipment', methods=['POST'])
def filter_equipment():
    if 'username' not in session:
        return redirect(url_for('login'))
    criteria = {
        'condition': request.form.get('condition', ''),
        'availability': request.form.get('availability', '')
    }
    results = EquipmentController.filter_equipment(criteria)
    return render_template('dashboard.html', 
                         username=session['username'],
                         equipment=results,
                         alerts=FileStorage.read_alerts())

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8110, debug=False)
