from flask import Flask, render_template, request, redirect, session
from user import User
from product import Product
from cart import Cart
from order import Order

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Load users and products
users = User().load_users()
products = Product().load_products()
cart = Cart()

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
        return redirect('/')
    return render_template('register.html')

@app.route('/products')
def product_listing():
    return render_template('products.html', products=products)

@app.route('/cart')
def view_cart():
    return render_template('cart.html', items=cart.view_cart())

@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    product = next((p for p in products if p.id == product_id), None)
    if product:
        cart.add_item(product)
    return redirect('/cart')

@app.route('/checkout')
def checkout():
    return render_template('checkout.html')

@app.route('/confirm_order', methods=['POST'])
def confirm_order():
    user = next((u for u in users if u.username == session.get('username')), None)
    order = Order(user, cart.view_cart())
    order.save_order()
    return render_template('confirmation.html')

if __name__ == '__main__':
    app.run(port=8672, debug=False)
