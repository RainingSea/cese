from flask import Flask, render_template, request, redirect, url_for, session
from auth import AuthManager
from equipment import EquipmentManager

app = Flask(__name__)
app.secret_key = 'secret_key'

auth = AuthManager()
equipment = EquipmentManager()

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
        if auth.login(username, password):
            return redirect(url_for('dashboard'))
        return "Invalid credentials", 401
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if auth.register(username, password):
            return redirect(url_for('login'))
        return "Registration failed", 400
    return render_template('register.html')

@app.route('/logout')
def logout():
    auth.logout()
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    query = request.args.get('query', '')
    filter_type = request.args.get('filter_type', '')
    items = equipment.search(query, filter_type)
    return render_template('dashboard.html', equipment=items)

@app.route('/add', methods=['POST'])
def add_equipment():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    name = request.form['name']
    type = request.form['type']
    quantity = request.form['quantity']
    condition = request.form['condition']
    location = request.form['location']
    
    equipment.add_item(name, type, quantity, condition, location)
    return redirect(url_for('dashboard'))

@app.route('/update/<id>', methods=['GET', 'POST'])
def update_equipment(id):
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        field = request.form['field']
        value = request.form['value']
        equipment.update_item(id, field, value)
        return redirect(url_for('dashboard'))
    
    items = equipment.search('')
    item = next((i for i in items if i['id'] == id), None)
    if not item:
        return "Item not found", 404
    
    return render_template('update.html', item=item)

if __name__ == '__main__':
    app.run(port=8111, debug=False)
