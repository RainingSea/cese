from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

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
                return False
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
            return [line.strip().split(',') for line in file.readlines()]

    def add_equipment(self, name: str, type: str, quantity: int, condition: str, location: str) -> bool:
        self.equipment.append([name, type, str(quantity), condition, location])
        with open('equipment.txt', 'a') as file:
            file.write(f"{name},{type},{quantity},{condition},{location}\n")
        return True

    def update_equipment(self, name: str, quantity: int, condition: str, location: str) -> bool:
        for item in self.equipment:
            if item[0] == name:
                item[2] = str(quantity)
                item[3] = condition
                item[4] = location
                self.save_equipment()
                return True
        return False

    def search_equipment(self, query: str):
        return [item for item in self.equipment if query.lower() in item[0].lower()]

    def filter_equipment(self, condition: str, availability: bool):
        return [item for item in self.equipment if item[3] == condition]

    def save_equipment(self):
        with open('equipment.txt', 'w') as file:
            for item in self.equipment:
                file.write(','.join(item) + '\n')

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
    return render_template('registration.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.login(username, password):
            return render_template('dashboard.html', equipment=equipment_manager.equipment)
    return redirect(url_for('login'))

if __name__ == '__main__':
    user_manager = UserManager()
    equipment_manager = EquipmentManager()
    app.run(port=8423, debug=False)
