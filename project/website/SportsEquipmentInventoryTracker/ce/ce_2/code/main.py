from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

class UserManager:
    def __init__(self):
        self.users = self.load_users()

    def load_users(self):
        users = {}
        if os.path.exists('users.txt'):
            with open('users.txt', 'r') as file:
                for line in file:
                    username, password = line.strip().split('|')
                    users[username] = password
        return users

    def register(self, username: str, password: str) -> bool:
        if username in self.users:
            return False
        self.users[username] = password
        with open('users.txt', 'a') as file:
            file.write(f"{username}|{password}\n")
        return True

    def login(self, username: str, password: str) -> bool:
        return self.users.get(username) == password

class EquipmentManager:
    def __init__(self):
        self.equipment = self.load_equipment()

    def load_equipment(self):
        equipment = []
        if os.path.exists('equipment.txt'):
            with open('equipment.txt', 'r') as file:
                for line in file:
                    name, type_, quantity, condition, location = line.strip().split('|')
                    equipment.append({
                        'name': name,
                        'type': type_,
                        'quantity': int(quantity),
                        'condition': condition,
                        'location': location
                    })
        return equipment

    def add_equipment(self, name: str, type_: str, quantity: int, condition: str, location: str) -> bool:
        self.equipment.append({
            'name': name,
            'type': type_,
            'quantity': quantity,
            'condition': condition,
            'location': location
        })
        with open('equipment.txt', 'a') as file:
            file.write(f"{name}|{type_}|{quantity}|{condition}|{location}\n")
        return True

    def update_equipment(self, name: str, quantity: int, condition: str, location: str) -> bool:
        for item in self.equipment:
            if item['name'] == name:
                item['quantity'] = quantity
                item['condition'] = condition
                item['location'] = location
                self.save_equipment()
                return True
        return False

    def save_equipment(self):
        with open('equipment.txt', 'w') as file:
            for item in self.equipment:
                file.write(f"{item['name']}|{item['type']}|{item['quantity']}|{item['condition']}|{item['location']}\n")

    def get_equipment(self) -> list:
        return self.equipment

    def search_equipment(self, query: str) -> list:
        return [item for item in self.equipment if query.lower() in item['name'].lower()]

    def filter_equipment(self, criteria: str) -> list:
        return [item for item in self.equipment if item['condition'] == criteria]

user_manager = UserManager()
equipment_manager = EquipmentManager()

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
        name = request.form['name']
        type_ = request.form['type']
        quantity = request.form['quantity']
        condition = request.form['condition']
        location = request.form['location']
        equipment_manager.add_equipment(name, type_, int(quantity), condition, location)
    equipment = equipment_manager.get_equipment()
    return render_template('dashboard.html', equipment=equipment)

if __name__ == '__main__':
    app.run(port=8252, debug=False)
