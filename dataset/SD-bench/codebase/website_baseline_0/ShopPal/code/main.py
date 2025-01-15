from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def save(self) -> None:
        with open('users.txt', 'a') as f:
            f.write(f"{self.username}|{self.password}\n")

class Product:
    def __init__(self, name: str, description: str, price: float):
        self.name = name
        self.description = description
        self.price = price
        self.reviews = []

    def add_review(self, review: str) -> None:
        self.reviews.append(review)

class Collection:
    def __init__(self, user: User):
        self.user = user
        self.products = []

    def add_product(self, product: Product) -> None:
        self.products.append(product)

    def remove_product(self, product: Product) -> None:
        self.products.remove(product)

class ShopPal:
    def __init__(self):
        self.users = self.load_users()
        self.products = self.load_products()
        self.collections = []

    def load_users(self):
        users = []
        if os.path.exists('users.txt'):
            with open('users.txt', 'r') as f:
                for line in f:
                    username, password = line.strip().split('|')
                    users.append(User(username, password))
        return users

    def load_products(self):
        products = []
        if os.path.exists('products.txt'):
            with open('products.txt', 'r') as f:
                for line in f:
                    name, description, price = line.strip().split('|')
                    products.append(Product(name, description, float(price)))
        return products

    def register(self, username: str, password: str) -> User:
        user = User(username, password)
        user.save()
        self.users.append(user)
        return user

    def login(self, username: str, password: str) -> User:
        for user in self.users:
            if user.username == username and user.password == password:
                return user
        return None

    def create_collection(self, user: User) -> Collection:
        collection = Collection(user)
        self.collections.append(collection)
        return collection

    def search_products(self, query: str) -> list:
        return [product for product in self.products if query.lower() in product.name.lower()]

    def track_price_changes(self, product: Product, new_price: float) -> None:
        product.price = new_price

    def view_detailed_product_information(self, product: Product) -> dict:
        return {
            'name': product.name,
            'description': product.description,
            'price': product.price,
            'reviews': product.reviews
        }

    def receive_discount_notifications(self, user: User) -> None:
        # Placeholder for future implementation
        pass

shop_pal = ShopPal()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = shop_pal.login(username, password)
        if user:
            session['username'] = username
            return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        shop_pal.register(username, password)
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    user_collections = [collection for collection in shop_pal.collections if collection.user.username == session['username']]
    return render_template('dashboard.html', collections=user_collections, products=shop_pal.products)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/back_to_dashboard')
def back_to_dashboard():
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(port=8552, debug=False)
