from flask import Flask, render_template, request, redirect, session
from user_manager import UserManager
from product_manager import ProductManager
from order_manager import OrderManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'

user_manager = UserManager('users.txt')
product_manager = ProductManager('products.txt')
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
            return redirect('/')
    return render_template('registration.html')

@app.route('/product_listing')
def product_listing():
    products = product_manager.get_product_list()
    return render_template('product_listing.html', products=products)

@app.route('/add_to_cart/<product_id>')
def add_to_cart(product_id):
    cart = session.get('cart', [])
    cart.append(product_id)
    session['cart'] = cart
    return redirect('/product_listing')

@app.route('/shopping_cart')
def shopping_cart():
    cart = session.get('cart', [])
    return render_template('shopping_cart.html', cart=cart)

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        user = session.get('username')
        cart = session.get('cart', [])
        order_manager.create_order(user, cart)
        session['cart'] = []
        return redirect('/order_confirmation')
    return render_template('checkout.html')

@app.route('/order_confirmation')
def order_confirmation():
    return render_template('order_confirmation.html')

if __name__ == '__main__':
    app.run(port=8669, debug=False)
