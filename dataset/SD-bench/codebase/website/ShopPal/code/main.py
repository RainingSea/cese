from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = generate_password_hash(password)

    def save(self) -> None:
        with open('users.txt', 'a') as f:
            f.write(f"{self.username}|{self.password}\n")

    @staticmethod
    def load(username: str) -> 'User':
        with open('users.txt', 'r') as f:
            for line in f:
                user_data = line.strip().split('|')
                if user_data[0] == username:
                    return User(user_data[0], user_data[1])
        return None

class Product:
    def __init__(self, name: str, description: str, price: float):
        self.name = name
        self.description = description
        self.price = price
        self.reviews = []

    def save(self) -> None:
        with open('products.txt', 'a') as f:
            f.write(f"{self.name}|{self.description}|{self.price}\n")

    @staticmethod
    def load(name: str) -> 'Product':
        with open('products.txt', 'r') as f:
            for line in f:
                product_data = line.strip().split('|')
                if product_data[0] == name:
                    return Product(product_data[0], product_data[1], float(product_data[2]))
        return None

class Collection:
    def __init__(self, user: User):
        self.user = user
        self.products = []

    def add_product(self, product: Product) -> None:
        self.products.append(product)

    def remove_product(self, product_name: str) -> None:
        self.products = [p for p in self.products if p.name != product_name]

    def save(self) -> None:
        with open('collections.txt', 'a') as f:
            f.write(f"{self.user.username}|{','.join([p.name for p in self.products])}\n")

    @staticmethod
    def load(user: User) -> 'Collection':
        with open('collections.txt', 'r') as f:
            for line in f:
                collection_data = line.strip().split('|')
                if collection_data[0] == user.username:
                    collection = Collection(user)
                    for product_name in collection_data[1].split(','):
                        product = Product.load(product_name)
                        if product:
                            collection.add_product(product)
                    return collection
        return None

class ShopPal:
    def __init__(self):
        self.users = []
        self.products = []
        self.collections = []

    def register(self, username: str, password: str) -> str:
        if User.load(username):
            return "Username already exists."
        user = User(username, password)
        user.save()
        return "Registration successful."

    def login(self, username: str, password: str) -> User:
        user = User.load(username)
        if user and check_password_hash(user.password, password):
            return user
        return None

    def search_product(self, query: str) -> list:
        results = []
        with open('products.txt', 'r') as f:
            for line in f:
                product_data = line.strip().split('|')
                if query.lower() in product_data[0].lower() or query.lower() in product_data[1].lower():
                    results.append(Product(product_data[0], product_data[1], float(product_data[2])))
        return results

    def track_price(self, product_name: str) -> None:
        # Implement price tracking logic here
        pass

@app.route('/', methods=['GET', 'POST'])
def login_route():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        shop_pal = ShopPal()
        user = shop_pal.login(username, password)
        if user:
            session['username'] = user.username
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials. Please try again.')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register_route():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        shop_pal = ShopPal()
        message = shop_pal.register(username, password)
        flash(message)
        if message == "Registration successful.":
            return redirect(url_for('login_route'))
    return render_template('registration.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login_route'))
    return render_template('dashboard.html')

@app.route('/product/<product_name>')
def product_detail(product_name):
    product = Product.load(product_name)
    return render_template('product_detail.html', product=product)

@app.route('/collection', methods=['GET', 'POST'])
def collection_route():
    if request.method == 'POST':
        username = request.form['username']
        product_name = request.form['product_name']
        shop_pal = ShopPal()
        user = shop_pal.login(username, 'dummy_password')  # Dummy password for loading collection
        if user:
            collection = Collection.load(user)
            if collection:
                product = Product.load(product_name)
                if product:
                    collection.add_product(product)
                    collection.save()
                    flash(f'Added {product_name} to your collection.')
                else:
                    flash('Product not found.')
            else:
                flash('Collection not found.')
        else:
            flash('User not found.')
    return render_template('collection.html')

@app.route('/search', methods=['GET', 'POST'])
def search_route():
    if request.method == 'POST':
        query = request.form['query']
        shop_pal = ShopPal()
        results = shop_pal.search_product(query)
        return render_template('search_results.html', results=results)
    return render_template('search.html')

@app.route('/logout')
def logout_route():
    session.pop('username', None)
    return redirect(url_for('login_route'))

if __name__ == '__main__':
    app.run(port=8697, debug=False)
