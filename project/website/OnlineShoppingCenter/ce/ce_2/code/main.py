from flask import Flask, render_template, request, redirect, url_for, session
from user import User
from product import Product
from shopping_cart import ShoppingCart
from checkout import Checkout

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Load users and products from text files
def load_data():
    users = User.load_users()
    products = Product.load_products()
    return users, products

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        new_user = User(username, password, email)
        new_user.save()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/product_listing')
def product_listing():
    _, products = load_data()
    return render_template('product_listing.html', products=products)

@app.route('/add_to_cart/<product_id>')
def add_to_cart(product_id):
    if 'cart' not in session:
        session['cart'] = ShoppingCart()
    session['cart'].add_item(product_id)
    return redirect(url_for('product_listing'))

@app.route('/shopping_cart')
def shopping_cart():
    cart = session.get('cart', ShoppingCart())
    return render_template('shopping_cart.html', items=cart.view_cart())

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        shipping_address = request.form['shipping_address']
        payment_info = request.form['payment_info']
        cart = session.get('cart', ShoppingCart())
        checkout = Checkout(shipping_address, payment_info)
        checkout.process_order(cart)
        return redirect(url_for('order_confirmation'))
    return render_template('checkout.html')

@app.route('/order_confirmation')
def order_confirmation():
    return render_template('order_confirmation.html')

if __name__ == '__main__':
    app.run(port=8671, debug=False)
