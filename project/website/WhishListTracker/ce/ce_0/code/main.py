from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

class WishlistTracker:
    def __init__(self):
        self.users = self.load_users()
        self.wishlist = self.load_wishlist()

    def load_users(self):
        users = {}
        if os.path.exists('users.txt'):
            with open('users.txt', 'r') as file:
                for line in file:
                    username, password = line.strip().split('|')
                    users[username] = password
        return users

    def load_wishlist(self):
        wishlist = {}
        if os.path.exists('wishlist.txt'):
            with open('wishlist.txt', 'r') as file:
                for line in file:
                    item_name, description, price = line.strip().split('|')
                    wishlist[item_name] = {'description': description, 'price': float(price)}
        return wishlist

    def register(self, username: str, password: str) -> bool:
        if username in self.users:
            return False
        self.users[username] = password
        with open('users.txt', 'a') as file:
            file.write(f"{username}|{password}\n")
        return True

    def login(self, username: str, password: str) -> bool:
        return self.users.get(username) == password

    def add_item(self, username: str, item_name: str, description: str, price: float) -> None:
        self.wishlist[item_name] = {'description': description, 'price': price}
        with open('wishlist.txt', 'a') as file:
            file.write(f"{item_name}|{description}|{price}\n")

    def view_wishlist(self, username: str) -> list:
        return self.wishlist

    def update_item(self, username: str, item_name: str, new_description: str, new_price: float) -> None:
        if item_name in self.wishlist:
            self.wishlist[item_name] = {'description': new_description, 'price': new_price}
            self.save_wishlist()

    def remove_item(self, username: str, item_name: str) -> None:
        if item_name in self.wishlist:
            del self.wishlist[item_name]
            self.save_wishlist()

    def save_wishlist(self):
        with open('wishlist.txt', 'w') as file:
            for item_name, details in self.wishlist.items():
                file.write(f"{item_name}|{details['description']}|{details['price']}\n")

tracker = WishlistTracker()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if tracker.register(username, password):
            return redirect(url_for('login'))
        else:
            return "Username already exists!"
    return render_template('registration.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if tracker.login(username, password):
            if 'add_item' in request.form:
                item_name = request.form['item_name']
                description = request.form['description']
                price = float(request.form['price'])
                tracker.add_item(username, item_name, description, price)
            return render_template('dashboard.html', wishlist=tracker.view_wishlist(username))
        else:
            return "Invalid credentials!"
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run(port=8286, debug=False)
