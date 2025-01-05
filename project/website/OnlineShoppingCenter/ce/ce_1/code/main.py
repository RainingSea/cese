from flask import Flask, render_template, request, redirect, url_for, session
from user import User
from product import Product
from order import Order

app = Flask(__name__)
app.secret_key = "your_secret_key"  # For session management

# Load users and products from text files at startup
users = User.load_users()
products = Product.load_products()

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
    return render_template('registration.html')

@app.route('/product_listing')
def product_listing():
    return render_template('product_listing.html', products=products)

@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    if 'cart' not in session:
        session['cart'] = []
    session['cart'].append(product_id)
    return redirect(url_for('product_listing'))

@app.route('/shopping_cart')
def shopping_cart():
    cart_products = [products[item] for item in session.get('cart', [])]
    return render_template('shopping_cart.html', cart_products=cart_products)

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        total = sum(products[item].price for item in session.get('cart', []))
        order = Order(User(request.form['username'], '', ''), session['cart'])
        order.save_order()
        session.pop('cart', None)  # Clear the cart after order is placed
        return redirect(url_for('order_confirmation'))
    return render_template('checkout.html')

@app.route('/order_confirmation')
def order_confirmation():
    return render_template('order_confirmation.html')

if __name__ == '__main__':
    app.run(port=8058, debug=False)
