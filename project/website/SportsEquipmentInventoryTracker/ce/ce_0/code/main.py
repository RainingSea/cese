from flask import Flask, render_template, request, redirect, session
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
        self.save_users()
        return True

    def save_users(self):
        with open('users.txt', 'w') as file:
            for user in self.users:
                file.write('|'.join(user) + '\n')

    def login(self, username: str, password: str) -> bool:
        for user in self.users:
            if user[0] == username and user[1] == password:
                session['username'] = username
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
        self.save_equipment()
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

    def filter_equipment(self, criteria: str):
        return [item for item in self.equipment if criteria.lower() in item[1].lower()]

    def save_equipment(self):
        with open('equipment.txt', 'w') as file:
            for item in self.equipment:
                file.write('|'.join(item) + '\n')

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    user_manager = UserManager()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            return redirect('/')
    return render_template('register.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    user_manager = UserManager()
    equipment_manager = EquipmentManager()
    if 'username' not in session:
        return redirect('/')
    if request.method == 'POST':
        name = request.form['name']
        type = request.form['type']
        quantity = int(request.form['quantity'])
        condition = request.form['condition']
        location = request.form['location']
        equipment_manager.add_equipment(name, type, quantity, condition, location)
    equipment_list = equipment_manager.equipment
    return render_template('dashboard.html', equipment=equipment_list)

@app.route('/login', methods=['POST'])
def do_login():
    user_manager = UserManager()
    username = request.form['username']
    password = request.form['password']
    if user_manager.login(username, password):
        return redirect('/dashboard')
    return redirect('/')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(port=8422, debug=False)
