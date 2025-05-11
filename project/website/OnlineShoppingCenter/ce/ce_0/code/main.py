from flask import Flask, render_template, request, redirect, url_for, session
from UserManager import UserManager
from ProductManager import ProductManager
from CartManager import CartManager
from OrderManager import OrderManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'

user_manager = UserManager('users.txt')
product_manager = ProductManager('products.txt')
cart_manager = CartManager('cart.txt')
order_manager = OrderManager('orders.txt')

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        if user_manager.register(username, password, email):
            return redirect(url_for('login'))
    return render_template('registration.html')

@app.route('/product_listing')
def product_listing():
    products = product_manager.load_products()
    return render_template('product_listing.html', products=products)

@app.route('/add_to_cart/<product_id>', methods=['POST'])
def add_to_cart(product_id):
    if 'username' in session:
        cart_manager.add_to_cart(session['username'], product_id)
    return redirect(url_for('product_listing'))

@app.route('/shopping_cart')
def shopping_cart():
    if 'username' in session:
        cart_items = cart_manager.load_cart(session['username'])
        return render_template('shopping_cart.html', cart_items=cart_items)
    return redirect(url_for('login'))

@app.route('/remove_from_cart/<product_id>', methods=['POST'])
def remove_from_cart(product_id):
    if 'username' in session:
        cart_manager.remove_from_cart(session['username'], product_id)
    return redirect(url_for('shopping_cart'))

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        shipping_address = request.form['shipping_address']
        payment_info = request.form['payment_info']
        if 'username' in session:
            cart_items = cart_manager.load_cart(session['username'])
            if order_manager.create_order(session['username'], cart_items, shipping_address, payment_info):
                return redirect(url_for('order_confirmation'))
    return render_template('checkout.html')

@app.route('/order_confirmation')
def order_confirmation():
    return render_template('order_confirmation.html')

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    if user_manager.login(username, password):
        session['username'] = username
        return redirect(url_for('product_listing'))
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8484, debug=False)
