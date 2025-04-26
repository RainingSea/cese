from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
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

class ProductManager:
    def __init__(self):
        self.collections = self.load_collections()

    def load_collections(self):
        if not os.path.exists('collections.txt'):
            return []
        with open('collections.txt', 'r') as file:
            return [line.strip().split('|') for line in file.readlines()]

    def add_product_to_collection(self, username: str, product: str) -> None:
        self.collections.append([username, product])
        with open('collections.txt', 'a') as file:
            file.write(f"{username}|{product}\n")

    def track_price_changes(self, username: str) -> None:
        # Placeholder for tracking price changes logic
        pass

    def search_products(self, query: str) -> list:
        return [collection for collection in self.collections if query in collection[1]]

user_manager = UserManager()
product_manager = ProductManager()

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
    return render_template('registration.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    user_collections = [collection for collection in product_manager.collections if collection[0] == session['username']]
    return render_template('dashboard.html', collections=user_collections)

if __name__ == '__main__':
    app.run(port=8238, debug=False)
