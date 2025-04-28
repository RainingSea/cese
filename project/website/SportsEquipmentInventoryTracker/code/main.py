from flask import Flask, render_template, request, redirect, url_for, flash, session
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class UserManager:
    def __init__(self, users_file):
        self.users_file = users_file
        self.load_users()

    def load_users(self):
        self.users = {}
        if os.path.exists(self.users_file):
            with open(self.users_file, 'r') as file:
                for line in file:
                    username, password = line.strip().split('|')
                    self.users[username] = password

    def register(self, username: str, password: str) -> bool:
        if username in self.users:
            return False
        self.users[username] = password
        with open(self.users_file, 'a') as file:
            file.write(f"{username}|{password}\n")
        return True

    def login(self, username: str, password: str) -> bool:
        return self.users.get(username) == password

class EquipmentManager:
    def __init__(self, equipment_file, alerts_file):
        self.equipment_file = equipment_file
        self.alerts_file = alerts_file
        self.load_equipment()

    def load_equipment(self):
        self.equipment = []
        if os.path.exists(self.equipment_file):
            with open(self.equipment_file, 'r') as file:
                for line in file:
                    name, quantity, condition, availability, location = line.strip().split('|')
                    self.equipment.append({
                        'name': name,
                        'quantity': int(quantity),
                        'condition': condition,
                        'availability': availability,
                        'location': location
                    })

    def add_equipment(self, name: str, quantity: int, condition: str, availability: str, location: str) -> bool:
        self.equipment.append({
            'name': name,
            'quantity': quantity,
            'condition': condition,
            'availability': availability,
            'location': location
        })
        with open(self.equipment_file, 'a') as file:
            file.write(f"{name}|{quantity}|{condition}|{availability}|{location}\n")
        return True

    def update_equipment(self, name: str, quantity: int, condition: str, availability: str, location: str) -> bool:
        for item in self.equipment:
            if item['name'] == name:
                item.update({
                    'quantity': quantity,
                    'condition': condition,
                    'availability': availability,
                    'location': location
                })
                self.save_equipment()
                return True
        return False

    def save_equipment(self):
        with open(self.equipment_file, 'w') as file:
            for item in self.equipment:
                file.write(f"{item['name']}|{item['quantity']}|{item['condition']}|{item['availability']}|{item['location']}\n")

    def view_equipment(self):
        return self.equipment

    def set_alert(self, equipment_name: str, alert_type: str, alert_date: str) -> bool:
        with open(self.alerts_file, 'a') as file:
            file.write(f"{equipment_name}|{alert_type}|{alert_date}\n")
        return True

    def search_equipment(self, query: str):
        return [item for item in self.equipment if query.lower() in item['name'].lower()]

    def filter_equipment(self, criteria: str):
        return [item for item in self.equipment if item['condition'] == criteria]

user_manager = UserManager('users.txt')
equipment_manager = EquipmentManager('equipment.txt', 'alerts.txt')

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.login(username, password):
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials. Please try again.')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            flash('Registration successful! You can now log in.')
            return redirect(url_for('login'))
        else:
            flash('Username already exists. Please choose another one.')
    return render_template('registration.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'username' not in session:
        return redirect('/')
    
    if request.method == 'POST':
        if 'update' in request.form:
            name = request.form['name']
            quantity = int(request.form['quantity'])
            condition = request.form['condition']
            availability = request.form['availability']
            location = request.form['location']
            equipment_manager.update_equipment(name, quantity, condition, availability, location)
        else:
            name = request.form['name']
            quantity = int(request.form['quantity'])
            condition = request.form['condition']
            availability = request.form['availability']
            location = request.form['location']
            equipment_manager.add_equipment(name, quantity, condition, availability, location)

    equipment = equipment_manager.view_equipment()
    return render_template('dashboard.html', equipment=equipment)

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '')
    results = equipment_manager.search_equipment(query)
    return render_template('search_results.html', results=results)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(port=8425, debug=False)
