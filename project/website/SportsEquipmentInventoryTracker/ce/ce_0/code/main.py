from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class UserManager:
    def __init__(self):
        self.users = self.load_users()

    def load_users(self):
        if not os.path.exists('users.txt'):
            return []
        with open('users.txt', 'r') as file:
            return [line.strip().split('|') for line in file.readlines()]

    def register(self, username: str, password: str) -> bool:
        for user in self.users:
            if user[0] == username:
                return False  # User already exists
        self.users.append([username, password])
        with open('users.txt', 'a') as file:
            file.write(f"{username}|{password}\n")
        return True

    def login(self, username: str, password: str) -> bool:
        for user in self.users:
            if user[0] == username and user[1] == password:
                return True
        return False

class EquipmentManager:
    def __init__(self):
        self.equipment = self.load_equipment()

    def load_equipment(self):
        if not os.path.exists('equipment.txt'):
            return []
        with open('equipment.txt', 'r') as file:
            return [line.strip().split('|') for line in file.readlines()]

    def add_equipment(self, name: str, type: str, quantity: int, condition: str, location: str) -> bool:
        self.equipment.append([name, type, str(quantity), condition, location])
        with open('equipment.txt', 'a') as file:
            file.write(f"{name}|{type}|{quantity}|{condition}|{location}\n")
        return True

    def update_equipment(self, name: str, quantity: int, condition: str, location: str) -> bool:
        for eq in self.equipment:
            if eq[0] == name:
                eq[2] = str(quantity)
                eq[3] = condition
                eq[4] = location
                self.save_equipment()
                return True
        return False

    def search_equipment(self, query: str) -> list:
        return [eq for eq in self.equipment if query.lower() in eq[0].lower()]

    def filter_equipment(self, criteria: str) -> list:
        return [eq for eq in self.equipment if criteria.lower() in eq[3].lower()]

    def save_equipment(self):
        with open('equipment.txt', 'w') as file:
            for eq in self.equipment:
                file.write(f"{'|'.join(eq)}\n")

user_manager = UserManager()
equipment_manager = EquipmentManager()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.login(username, password):
            session['username'] = username
            return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', equipment=equipment_manager.equipment)

if __name__ == '__main__':
    app.run(port=8250, debug=False)
