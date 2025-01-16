from flask import Flask, render_template, request, redirect, session
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class User:
    def __init__(self, username: str, password: str, email: str) -> None:
        self.username = username
        self.password = password
        self.email = email

    def save(self) -> None:
        with open('users.txt', 'a') as f:
            f.write(f"{self.username}|{self.password}|{self.email}\n")

    @staticmethod
    def load_users() -> list:
        users = []
        try:
            with open('users.txt', 'r') as f:
                for line in f:
                    username, password, email = line.strip().split('|')
                    users.append(User(username, password, email))
        except FileNotFoundError:
            pass
        return users

class Product:
    def __init__(self, id: int, name: str, price: float) -> None:
        self.id = id
        self.name = name
        self.price = price

    @staticmethod
    def load_products() -> list:
        products = []
        try:
            with open('products.txt', 'r') as f:
                for line in f:
                    id, name, price = line.strip().split('|')
                    products.append(Product(int(id), name, float(price)))
        except FileNotFoundError:
            pass
        return products

class ShoppingCart:
    def __init__(self, user_id: str) -> None:
        self.user_id = user_id
        self.items = []

    def add_item(self, product_id: int) -> None:
        self.items.append(product_id)

    def remove_item(self, product_id: int) -> None:
        if product_id in self.items:
            self.items.remove(product_id)

    def view_cart(self) -> list:
        return self.items

    def save_cart(self) -> None:
        with open('carts.txt', 'a') as f:
            f.write(f"{self.user_id}|{'|'.join(map(str, self.items))}\n")

class Order:
    def __init__(self, username: str, items: list, shipping_address: str, payment_info: str) -> None:
        self.username = username
        self.items = items
        self.shipping_address = shipping_address
        self.payment_info = payment_info

    def confirm_order(self) -> None:
        with open('orders.txt', 'a') as f:
            f.write(f"{self.username}|{'|'.join(map(str, self.items))}|{self.shipping_address}|{self.payment_info}\n")

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    users = User.load_users()
    for user in users:
        if user.username == username and user.password == password:
            session['username'] = username
            session['cart'] = ShoppingCart(username)  # Initialize cart on login
            return redirect('/products')
    return redirect('/')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        user = User(username, password, email)
        user.save()
        return redirect('/')
    return render_template('register.html')

@app.route('/products')
def products():
    product_list = Product.load_products()
    return render_template('products.html', products=product_list)

@app.route('/cart', methods=['GET', 'POST'])
def cart():
    if request.method == 'POST':
        product_id = int(request.form['product_id'])
        if 'cart' not in session:
            session['cart'] = ShoppingCart(session['username'])
        session['cart'].add_item(product_id)
        session.modified = True
    return render_template('cart.html', cart=session.get('cart', ShoppingCart(session['username'])).view_cart())

@app.route('/remove_from_cart', methods=['POST'])
def remove_from_cart():
    product_id = int(request.form['product_id'])
    if 'cart' in session:
        session['cart'].remove_item(product_id)
        session.modified = True
    return redirect('/cart')

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        shipping_address = request.form['shipping_address']
        payment_info = request.form['payment_info']
        order = Order(session['username'], session['cart'].view_cart(), shipping_address, payment_info)
        order.confirm_order()
        return redirect('/order_confirmation')
    return render_template('checkout.html')

@app.route('/order_confirmation')
def order_confirmation():
    return render_template('order_confirmation.html')

if __name__ == '__main__':
    app.run(port=8544, debug=False)
