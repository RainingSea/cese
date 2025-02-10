from flask import Flask, render_template, request, redirect, url_for, session
from user import User
from product import Product
from collection import Collection
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Load users from file
def load_users():
    users = {}
    if os.path.exists('users.txt'):
        with open('users.txt', 'r') as file:
            for line in file:
                username, password = line.strip().split('|')
                users[username] = password
    return users

# Load products from file
def load_products():
    products = {}
    if os.path.exists('products.txt'):
        with open('products.txt', 'r') as file:
            for line in file:
                name, description, price = line.strip().split('|')
                products[name] = Product(name, description, float(price))
    return products

# Load collections from file
def load_collections():
    collections = {}
    if os.path.exists('collections.txt'):
        with open('collections.txt', 'r') as file:
            for line in file:
                username, product_names = line.strip().split('|')
                product_list = product_names.split(',')
                collections[username] = Collection(User(username, ''), [load_products()[name] for name in product_list])
    return collections

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        with open('users.txt', 'a') as file:
            file.write(f"{username}|{password}\n")
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = load_users()
        if username in users and users[username] == password:
            session['username'] = username
            return render_template('dashboard.html', collections=load_collections().get(username, []))
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8694, debug=False)
