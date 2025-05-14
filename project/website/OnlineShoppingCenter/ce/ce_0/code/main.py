from flask import Flask, render_template, request, redirect, url_for, session
import os
import time
from UserManager import UserManager
from ProductManager import ProductManager
from CartManager import CartManager
from OrderManager import OrderManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'

user_manager = UserManager('users.txt')
product_manager = ProductManager('products.txt')
cart_manager = CartManager('carts.txt')
order_manager = OrderManager('orders.txt')

@app.route('/')
def home():
    if 'username' in session:
        return redirect(url_for('products'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.validate_user(username, password):
            session['username'] = username
            return redirect(url_for('products'))
        return render_template('login.html', error='Invalid credentials')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        if user_manager.add_user(username, password, email):
            return redirect(url_for('login'))
        return render_template('register.html', error='Username already exists')
    return render_template('register.html')

@app.route('/products')
def products():
    if 'username' not in session:
        return redirect(url_for('login'))
    products = product_manager.get_products()
    return render_template('products.html', products=products)

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    if 'username' not in session:
        return redirect(url_for('login'))
    product_id = request.form['product_id']
    cart_manager.add_item(session['username'], product_id)
    return redirect(url_for('products'))

@app.route('/cart')
def cart():
    if 'username' not in session:
        return redirect(url_for('login'))
    cart_items = cart_manager.get_cart(session['username'])
    products = product_manager.get_products()
    items = [p for p in products if str(p['id']) in cart_items]
    return render_template('cart.html', items=items)

@app.route('/remove_from_cart', methods=['POST'])
def remove_from_cart():
    if 'username' not in session:
        return redirect(url_for('login'))
    product_id = request.form['product_id']
    cart_manager.remove_item(session['username'], product_id)
    return redirect(url_for('cart'))

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        address = request.form['address']
        payment = request.form['payment']
        cart_items = cart_manager.get_cart(session['username'])
        order_id = str(int(time.time()))
        order_manager.create_order(session['username'], cart_items, address, payment)
        cart_manager.clear_cart(session['username'])
        return redirect(url_for('confirmation', order_id=order_id))
    return render_template('checkout.html')

@app.route('/confirmation/<order_id>')
def confirmation(order_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    order = order_manager.get_order(order_id)
    return render_template('confirmation.html', order=order)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8018, debug=False)
