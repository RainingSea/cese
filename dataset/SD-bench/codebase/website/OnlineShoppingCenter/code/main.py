from flask import Flask, render_template, request, redirect, session
from user import User
from product import Product
from cart import Cart
from order import Order

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Load users and products from files
users = User.load_all()
products = Product.load_all()
cart = Cart()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    for user in users:
        if user.username == username and user.password == password:
            session['user'] = username
            return redirect('/product_listing')
    return redirect('/')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        new_user = User(username, password, email)
        new_user.save()
        return redirect('/')
    return render_template('registration.html')

@app.route('/product_listing')
def browse_products():
    if not products:
        return render_template('product_listing.html', products=[], error="No products available.")
    return render_template('product_listing.html', products=products)

@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    cart.add_item(product_id)
    return redirect('/shopping_cart')

@app.route('/remove_from_cart/<int:product_id>')
def remove_from_cart(product_id):
    cart.remove_item(product_id)
    return redirect('/shopping_cart')

@app.route('/shopping_cart')
def shopping_cart():
    items = cart.get_items()
    return render_template('shopping_cart.html', items=items)

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        shipping_address = request.form['shipping_address']
        payment_info = request.form['payment_info']
        order = Order(len(Order.load_all()) + 1, session['user'], cart.get_items(), shipping_address, payment_info)
        order.save()
        cart.save()  # Save cart after checkout
        return redirect('/order_confirmation')
    return render_template('checkout.html')

@app.route('/order_confirmation')
def order_confirmation():
    return render_template('order_confirmation.html')

@app.route('/back_to_products')
def back_to_products():
    return redirect('/product_listing')

if __name__ == '__main__':
    app.run(port=8674, debug=False)
