from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'


class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def save(self):
        with open('users.txt', 'a') as f:
            f.write(f"{self.username}|{self.password}\n")

    @staticmethod
    def load_all():
        users = []
        if os.path.exists('users.txt'):
            with open('users.txt', 'r') as f:
                for line in f:
                    username, password = line.strip().split('|')
                    users.append(User(username, password))
        return users


class Product:
    def __init__(self, name: str, description: str, price: float):
        self.name = name
        self.description = description
        self.price = price

    def save(self):
        with open('products.txt', 'a') as f:
            f.write(f"{self.name}|{self.description}|{self.price}\n")

    @staticmethod
    def load_all():
        products = []
        if os.path.exists('products.txt'):
            with open('products.txt', 'r') as f:
                for line in f:
                    name, description, price = line.strip().split('|')
                    products.append(Product(name, description, float(price)))
        return products


class Collection:
    def __init__(self, user: str):
        self.user = user
        self.products = []

    def add_product(self, product: Product):
        self.products.append(product)

    def save(self):
        with open('collections.txt', 'a') as f:
            f.write(f"{self.user}|{','.join([p.name for p in self.products])}\n")

    @staticmethod
    def load(user: str):
        collections = []
        if os.path.exists('collections.txt'):
            with open('collections.txt', 'r') as f:
                for line in f:
                    u, products = line.strip().split('|')
                    if u == user:
                        product_names = products.split(',')
                        collections.append(Collection(u))
                        collections[-1].products = product_names
        return collections


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = User.load_all()
        for user in users:
            if user.username == username and user.password == password:
                session['username'] = username
                return redirect(url_for('dashboard'))
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User(username, password)
        user.save()
        return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/dashboard')
def dashboard():
    products = Product.load_all()
    return render_template('dashboard.html', products=products)


if __name__ == '__main__':
    app.run(port=8696, debug=False)
