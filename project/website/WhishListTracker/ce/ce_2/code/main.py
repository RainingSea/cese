from flask import Flask, render_template, request, redirect, session
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'

class UserManager:
    def __init__(self, filename):
        self.filename = filename
        self.load_users()

    def load_users(self):
        self.users = {}
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as file:
                for line in file:
                    username, password = line.strip().split('|')
                    self.users[username] = password

    def register(self, username: str, password: str) -> bool:
        if username in self.users:
            return False
        self.users[username] = password
        with open(self.filename, 'a') as file:
            file.write(f"{username}|{password}\n")
        return True

    def login(self, username: str, password: str) -> bool:
        return self.users.get(username) == password

class WishlistManager:
    def __init__(self, filename):
        self.filename = filename
        self.load_items()

    def load_items(self):
        self.items = []
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as file:
                for line in file:
                    item_name, description, price = line.strip().split('|')
                    self.items.append({'item_name': item_name, 'description': description, 'price': float(price)})

    def add_item(self, item_name: str, description: str, price: float) -> bool:
        self.items.append({'item_name': item_name, 'description': description, 'price': price})
        with open(self.filename, 'a') as file:
            file.write(f"{item_name}|{description}|{price}\n")
        return True

    def view_items(self) -> list:
        return self.items

    def update_item(self, item_name: str, description: str, price: float) -> bool:
        for item in self.items:
            if item['item_name'] == item_name:
                item['description'] = description
                item['price'] = price
                self.save_items()
                return True
        return False

    def remove_item(self, item_name: str) -> bool:
        self.items = [item for item in self.items if item['item_name'] != item_name]
        self.save_items()
        return True

    def save_items(self):
        with open(self.filename, 'w') as file:
            for item in self.items:
                file.write(f"{item['item_name']}|{item['description']}|{item['price']}\n")

user_manager = UserManager('users.txt')
wishlist_manager = WishlistManager('wishlist.txt')

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.login(username, password):
            session['username'] = username
            return redirect('/dashboard')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            return redirect('/')
    return render_template('registration.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'username' not in session:
        return redirect('/')
    if request.method == 'POST':
        if 'add' in request.form:
            item_name = request.form['item_name']
            description = request.form['description']
            price = float(request.form['price'])
            wishlist_manager.add_item(item_name, description, price)
        elif 'update' in request.form:
            item_name = request.form['item_name']
            description = request.form['description']
            price = float(request.form['price'])
            wishlist_manager.update_item(item_name, description, price)
        elif 'remove' in request.form:
            item_name = request.form['item_name']
            wishlist_manager.remove_item(item_name)
    items = wishlist_manager.view_items()
    return render_template('dashboard.html', items=items)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(port=8460, debug=False)
