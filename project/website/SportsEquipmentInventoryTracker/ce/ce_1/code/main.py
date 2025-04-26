from flask import Flask, render_template, request, redirect, url_for, session
from tools import load_users, load_equipment, save_users, save_equipment

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class UserManager:
    def __init__(self):
        self.users = load_users()

    def register(self, username: str, password: str) -> bool:
        if username in self.users:
            return False
        self.users[username] = password
        save_users(self.users)
        return True

    def login(self, username: str, password: str) -> bool:
        return self.users.get(username) == password

class EquipmentManager:
    def __init__(self):
        self.equipment = load_equipment()

    def add_equipment(self, name: str, type: str, quantity: int, condition: str, availability: bool, location: str) -> bool:
        self.equipment[name] = {
            'type': type,
            'quantity': quantity,
            'condition': condition,
            'availability': availability,
            'location': location
        }
        save_equipment(self.equipment)
        return True

    def update_equipment(self, name: str, quantity: int, condition: str, availability: bool, location: str) -> bool:
        if name not in self.equipment:
            return False
        self.equipment[name].update({
            'quantity': quantity,
            'condition': condition,
            'availability': availability,
            'location': location
        })
        save_equipment(self.equipment)
        return True

    def search_equipment(self, query: str):
        return {name: details for name, details in self.equipment.items() if query.lower() in name.lower()}

    def filter_equipment(self, criteria: str):
        return {name: details for name, details in self.equipment.items() if details['type'] == criteria}

    def set_alert(self, name: str) -> bool:
        # Placeholder for alert setting logic
        return True

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_manager = UserManager()
        if user_manager.login(username, password):
            session['username'] = username
            return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_manager = UserManager()
        if user_manager.register(username, password):
            return redirect(url_for('login'))
    return render_template('registration.html')

@app.route('/dashboard')
def dashboard():
    equipment_manager = EquipmentManager()
    equipment_list = equipment_manager.equipment
    return render_template('dashboard.html', equipment=equipment_list)

if __name__ == '__main__':
    app.run(port=8251, debug=False)
