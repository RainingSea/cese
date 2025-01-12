from flask import Flask, render_template, request, redirect, url_for, session
import json
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class User:
    def __init__(self, username: str, password: str, email: str):
        self.username = username
        self.password = password
        self.email = email

    def save(self):
        users = self.load_all()
        users.append(self.__dict__)
        with open('users.txt', 'w') as f:
            json.dump(users, f)

    @staticmethod
    def load_all():
        if os.path.exists('users.txt'):
            with open('users.txt', 'r') as f:
                return json.load(f)
        return []

    @staticmethod
    def authenticate(username: str, password: str):
        users = User.load_all()
        for user in users:
            if user['username'] == username and user['password'] == password:
                return user
        return None

class Product:
    def __init__(self, id: int, name: str, price: float):
        self.id = id
        self.name = name
        self.price = price

    @staticmethod
    def load_all():
        if os.path.exists('products.txt'):
            with open('products.txt', 'r') as f:
                return json.load(f)
        return []

class Cart:
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.items = []

    def add_item(self, product_id: int):
        self.items.append(product_id)

    def remove_item(self, product_id: int):
        if product_id in self.items:
            self.items.remove(product_id)

    def save(self):
        carts = self.load()
        carts[self.user_id] = self.items
        with open('carts.txt', 'w') as f:
            json.dump(carts, f)

    @staticmethod
    def load():
        if os.path.exists('carts.txt'):
            with open('carts.txt', 'r') as f:
                return json.load(f)
        return {}

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    user = User.authenticate(username, password)
    if user:
        session['user_id'] = user['username']
        return redirect(url_for('product_listing'))
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        user = User(username, password, email)
        user.save()
        return redirect(url_for('login'))
    return render_template('registration.html')

@app.route('/products')
def product_listing():
    products = Product.load_all()
    return render_template('product_listing.html', products=products)

@app.route('/cart')
def shopping_cart():
    user_id = session.get('user_id')
    cart = Cart(user_id)
    cart_data = cart.load().get(user_id, [])
    return render_template('shopping_cart.html', cart_items=cart_data)

@app.route('/cart/add/<int:product_id>')
def add_to_cart(product_id):
    user_id = session.get('user_id')
    cart = Cart(user_id)
    cart.add_item(product_id)
    cart.save()
    return redirect(url_for('product_listing'))

@app.route('/cart/remove/<int:product_id>')
def remove_from_cart(product_id):
    user_id = session.get('user_id')
    cart = Cart(user_id)
    cart.remove_item(product_id)
    cart.save()
    return redirect(url_for('shopping_cart'))

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        shipping_address = request.form['shipping_address']
        payment_info = request.form['payment_info']
        user_id = session.get('user_id')
        cart = Cart(user_id)
        cart_data = cart.load().get(user_id, [])
        # Assuming Order is defined similarly to User and Product
        order = Order(user_id, cart_data, shipping_address, payment_info)
        order.confirm_order()
        return redirect(url_for('order_confirmation'))
    return render_template('checkout.html')

@app.route('/order_confirmation')
def order_confirmation():
    return render_template('order_confirmation.html')

if __name__ == '__main__':
    app.run(port=8315, debug=False)
