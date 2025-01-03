from flask import Flask, render_template, request, redirect, url_for, session
from typing import List
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class User:
    def __init__(self, username: str, password: str, email: str):
        self.username = username
        self.password = password
        self.email = email

    def save(self) -> None:
        with open('users.txt', 'a') as f:
            f.write(f"{self.username}|{self.password}|{self.email}\n")

class Product:
    def __init__(self, id: int, name: str, price: float):
        self.id = id
        self.name = name
        self.price = price

    def to_string(self) -> str:
        return f"{self.id}|{self.name}|{self.price}"

class ShoppingCart:
    def __init__(self):
        self.items = {}

    def add_item(self, product: Product) -> None:
        if product.id in self.items:
            self.items[product.id]['quantity'] += 1
        else:
            self.items[product.id] = {'product': product, 'quantity': 1}

    def remove_item(self, product_id: int) -> None:
        if product_id in self.items:
            del self.items[product_id]

    def get_items(self) -> dict:
        return self.items

    def clear(self) -> None:
        self.items.clear()

class Order:
    def __init__(self, user: User, items: dict, shipping_address: str, payment_info: str):
        self.user = user
        self.items = items
        self.shipping_address = shipping_address
        self.payment_info = payment_info

    def save(self) -> None:
        with open('orders.txt', 'a') as f:
            order_summary = f"{self.user.username}|{self.shipping_address}|{self.payment_info}|"
            order_items = ','.join([f"{item['product'].name} (Quantity: {item['quantity']})" for item in self.items.values()])
            f.write(f"{order_summary}{order_items}\n")

class Application:
    def __init__(self):
        self.users = self.load_users()
        self.products = self.load_products()
        self.shopping_cart = ShoppingCart()

    def load_users(self) -> List[User]:
        users = []
        if os.path.exists('users.txt'):
            with open('users.txt', 'r') as f:
                for line in f:
                    username, password, email = line.strip().split('|')
                    users.append(User(username, password, email))
        return users

    def load_products(self) -> List[Product]:
        products = []
        if os.path.exists('products.txt'):
            with open('products.txt', 'r') as f:
                for line in f:
                    id, name, price = line.strip().split('|')
                    products.append(Product(int(id), name, float(price)))
        return products

    def browse_products(self) -> List[Product]:
        return self.products

    def register_user(self, username: str, password: str, email: str) -> None:
        new_user = User(username, password, email)
        new_user.save()
        self.users.append(new_user)

    def login_user(self, username: str, password: str) -> User:
        for user in self.users:
            if user.username == username and user.password == password:
                return user
        return None

app_instance = Application()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        app_instance.register_user(username, password, email)
        return redirect(url_for('login'))
    return render_template('registration.html')

@app.route('/login', methods=['POST'])
def login_user():
    username = request.form['username']
    password = request.form['password']
    user = app_instance.login_user(username, password)
    if user:
        session['username'] = user.username
        return redirect(url_for('product_listing'))
    return redirect(url_for('login'))

@app.route('/products')
def product_listing():
    products = app_instance.browse_products()
    return render_template('product_listing.html', products=products)

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    product_id = int(request.form['product_id'])
    product = next((p for p in app_instance.products if p.id == product_id), None)
    if product:
        app_instance.shopping_cart.add_item(product)
    return redirect(url_for('product_listing'))

@app.route('/cart')
def view_cart():
    items = app_instance.shopping_cart.get_items()
    return render_template('shopping_cart.html', items=items)

@app.route('/remove_from_cart/<int:product_id>')
def remove_from_cart(product_id):
    app_instance.shopping_cart.remove_item(product_id)
    return redirect(url_for('view_cart'))

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        shipping_address = request.form['shipping_address']
        payment_info = request.form['payment_info']
        user = next((u for u in app_instance.users if u.username == session['username']), None)
        order = Order(user, app_instance.shopping_cart.get_items(), shipping_address, payment_info)
        order.save()
        app_instance.shopping_cart.clear()
        return redirect(url_for('order_confirmation'))
    return render_template('checkout.html')

@app.route('/order_confirmation')
def order_confirmation():
    return render_template('order_confirmation.html')

if __name__ == '__main__':
    app.run(debug=True)