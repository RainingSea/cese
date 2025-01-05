from flask import Flask, render_template, request, redirect, session
from user import User
from product import Product
from order import Order

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Load users and products from files
def load_users():
    users = []
    with open('users.txt', 'r') as file:
        for line in file:
            username, password, email = line.strip().split('|')
            users.append(User(username, password, email))
    return users

def load_products():
    products = []
    with open('products.txt', 'r') as file:
        for line in file:
            id, name, price, description = line.strip().split('|')
            products.append(Product(int(id), name, float(price), description))
    return products

users = load_users()
products = load_products()

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
        users.append(new_user)
        with open('users.txt', 'a') as file:
            file.write(f"{username}|{password}|{email}\n")
        return redirect('/')
    return render_template('registration.html')

@app.route('/product_listing')
def product_listing():
    return render_template('product_listing.html', products=products)

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    for user in users:
        if user.username == username and user.password == password:
            session['username'] = username
            return redirect('/product_listing')
    return redirect('/')

@app.route('/shopping_cart')
def shopping_cart():
    return render_template('shopping_cart.html')

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        # Process checkout logic here
        return redirect('/order_confirmation')
    return render_template('checkout.html')

@app.route('/order_confirmation')
def order_confirmation():
    return render_template('order_confirmation.html')

if __name__ == '__main__':
    app.run(port=8059, debug=False)
