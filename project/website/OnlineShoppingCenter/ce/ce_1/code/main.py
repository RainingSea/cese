from flask import Flask, render_template, request, redirect, url_for, session
from UserManager import UserManager
from ProductManager import ProductManager
from CartManager import CartManager
from OrderManager import OrderManager

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # For session management

user_manager = UserManager('users.txt')
product_manager = ProductManager('products.txt')
cart_manager = CartManager('cart.txt')
order_manager = OrderManager('orders.txt')

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def user_login():
    username = request.form['username']
    password = request.form['password']
    if user_manager.login(username, password):
        session['username'] = username
        return redirect(url_for('product_listing'))
    return render_template('login.html', error='Invalid credentials')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        if user_manager.register(username, password, email):
            return redirect(url_for('login'))
        return render_template('registration.html', error='User already exists')
    return render_template('registration.html')

@app.route('/product_listing')
def product_listing():
    products = product_manager.get_products()
    return render_template('product_listing.html', products=products)

@app.route('/add_to_cart/<product_id>')
def add_to_cart(product_id):
    if 'username' in session:
        cart_manager.add_to_cart(session['username'], product_id)
    return redirect(url_for('product_listing'))

@app.route('/remove_from_cart/<product_id>')
def remove_from_cart(product_id):
    if 'username' in session:
        cart_manager.remove_from_cart(session['username'], product_id)
    return redirect(url_for('shopping_cart'))

@app.route('/shopping_cart')
def shopping_cart():
    if 'username' in session:
        cart_items = cart_manager.get_cart(session['username'])
        return render_template('shopping_cart.html', cart_items=cart_items)
    return redirect(url_for('login'))

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        shipping_info = request.form['shipping_info']
        product_ids = cart_manager.get_cart(session['username'])
        order_manager.create_order(session['username'], product_ids, shipping_info)
        return redirect(url_for('order_confirmation'))
    return render_template('checkout.html')

@app.route('/order_confirmation')
def order_confirmation():
    return render_template('order_confirmation.html')

if __name__ == '__main__':
    user_manager.load_users()
    product_manager.load_products()
    cart_manager.load_cart()
    app.run(port=8485, debug=False)
