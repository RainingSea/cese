from flask import Flask, render_template, request, redirect, url_for, session
from UserManager import UserManager
from ProductManager import ProductManager
from CartManager import CartManager
from OrderManager import OrderManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'

user_manager = UserManager()
product_manager = ProductManager()
cart_manager = CartManager()
order_manager = OrderManager()

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

@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    username = session.get('username')
    if username:
        cart_manager.add_to_cart(username, product_id)
    return redirect(url_for('product_listing'))

@app.route('/shopping_cart')
def shopping_cart():
    username = session.get('username')
    if username:
        cart_items = cart_manager.view_cart(username)
        return render_template('shopping_cart.html', cart_items=cart_items)
    return redirect(url_for('login'))

@app.route('/remove_from_cart/<int:product_id>')
def remove_from_cart(product_id):
    username = session.get('username')
    if username:
        cart_manager.remove_from_cart(username, product_id)
    return redirect(url_for('shopping_cart'))

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    username = session.get('username')
    if not username:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        shipping_info = {
            'address': request.form['address'],
            'payment_method': request.form['payment_method']
        }
        cart_items = cart_manager.view_cart(username)
        order_manager.create_order(username, cart_items, shipping_info)
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

if __name__ == '__main__':
    app.run(port=8486, debug=False)
