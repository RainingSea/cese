from flask import Flask, render_template, request, redirect, session, flash
from flask_session import Session
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

class UserManager:
    def __init__(self, filename='users.txt'):
        self.filename = filename
        self.users = self.load_users()

    def register(self, username: str, password: str) -> bool:
        if username in self.users:
            return False
        self.users[username] = password
        with open(self.filename, 'a') as f:
            f.write(f"{username},{password}\n")
        return True

    def login(self, username: str, password: str) -> bool:
        return self.users.get(username) == password

    def load_users(self) -> dict:
        if not os.path.exists(self.filename):
            return {}
        with open(self.filename, 'r') as f:
            return {line.split(',')[0]: line.split(',')[1].strip() for line in f.readlines()}

    def logout(self) -> None:
        session.pop('username', None)

class ProductManager:
    def __init__(self, collection_file='collections.txt', price_file='price_tracking.txt'):
        self.collection_file = collection_file
        self.price_file = price_file
        self.collections = self.load_collections()
        self.price_tracking = self.load_price_tracking()

    def create_collection(self, username: str, products: list) -> bool:
        with open(self.collection_file, 'a') as f:
            f.write(f"{username},{','.join(products)}\n")
        self.collections.append(f"{username},{','.join(products)}")
        return True

    def track_price_change(self, product_id: str, new_price: float) -> bool:
        with open(self.price_file, 'a') as f:
            f.write(f"{product_id},{new_price}\n")
        self.price_tracking.append(f"{product_id},{new_price}")
        return True

    def search_products(self, query: str) -> list:
        return [collection for collection in self.collections if query in collection]

    def load_collections(self) -> list:
        if not os.path.exists(self.collection_file):
            return []
        with open(self.collection_file, 'r') as f:
            return [line.strip() for line in f.readlines()]

    def load_price_tracking(self) -> list:
        if not os.path.exists(self.price_file):
            return []
        with open(self.price_file, 'r') as f:
            return [line.strip() for line in f.readlines()]

user_manager = UserManager()
product_manager = ProductManager()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.login(username, password):
            session['username'] = username
            return redirect('/dashboard')
        else:
            flash('Invalid credentials. Please try again.')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            flash('Registration successful! Please log in.')
            return redirect('/')
        else:
            flash('Username already exists. Please choose another.')
    return render_template('registration.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'username' not in session:
        return redirect('/')
    collections = product_manager.load_collections()
    if request.method == 'POST':
        search_query = request.form['search']
        collections = product_manager.search_products(search_query)
    return render_template('dashboard.html', collections=collections)

@app.route('/product/<product_id>')
def product_detail(product_id):
    return render_template('product_detail.html', product_id=product_id)

@app.route('/logout')
def logout():
    user_manager.logout()
    flash('You have been logged out.')
    return redirect('/')

if __name__ == '__main__':
    app.run(port=8241, debug=False)
