from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

class WishlistItem:
    def __init__(self, item_name: str, description: str, price: float):
        self.item_name = item_name
        self.description = description
        self.price = price

class WishlistTracker:
    def register(self, username: str, password: str) -> bool:
        if self._user_exists(username):
            return False
        with open('users.txt', 'a') as f:
            f.write(f"{username}|{password}\n")
        return True

    def login(self, username: str, password: str) -> bool:
        with open('users.txt', 'r') as f:
            for line in f:
                user, pwd = line.strip().split('|')
                if user == username and pwd == password:
                    return True
        return False

    def add_item(self, username: str, item_name: str, description: str, price: float) -> None:
        with open(f'wishlist_{username}.txt', 'a') as f:
            f.write(f"{item_name}|{description}|{price}\n")

    def view_wishlist(self, username: str) -> list:
        if not os.path.exists(f'wishlist_{username}.txt'):
            return []
        with open(f'wishlist_{username}.txt', 'r') as f:
            return [line.strip().split('|') for line in f]

    def update_item(self, username: str, old_item_name: str, new_item_name: str, new_description: str, new_price: float) -> None:
        items = self.view_wishlist(username)
        updated_items = []
        for item in items:
            if item[0] == old_item_name:
                updated_items.append(f"{new_item_name}|{new_description}|{new_price}")
            else:
                updated_items.append(f"{item[0]}|{item[1]}|{item[2]}")
        with open(f'wishlist_{username}.txt', 'w') as f:
            for item in updated_items:
                f.write(f"{item}\n")

    def remove_item(self, username: str, item_name: str) -> None:
        items = self.view_wishlist(username)
        updated_items = [item for item in items if item[0] != item_name]
        with open(f'wishlist_{username}.txt', 'w') as f:
            for item in updated_items:
                f.write(f"{item[0]}|{item[1]}|{item[2]}\n")

    def _user_exists(self, username: str) -> bool:
        with open('users.txt', 'r') as f:
            for line in f:
                if line.strip().split('|')[0] == username:
                    return True
        return False

tracker = WishlistTracker()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if tracker.login(username, password):
            session['username'] = username
            return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if tracker.register(username, password):
            return redirect(url_for('login'))
    return render_template('registration.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    username = session['username']
    if request.method == 'POST':
        if 'add_item' in request.form:
            item_name = request.form['item_name']
            description = request.form['description']
            price = request.form['price']
            tracker.add_item(username, item_name, description, float(price))
        elif 'remove_item' in request.form:
            item_name = request.form['item_name']
            tracker.remove_item(username, item_name)
        elif 'update_item' in request.form:
            old_item_name = request.form['old_item_name']
            new_item_name = request.form['new_item_name']
            new_description = request.form['new_description']
            new_price = request.form['new_price']
            tracker.update_item(username, old_item_name, new_item_name, new_description, float(new_price))

    wishlist = tracker.view_wishlist(username)
    return render_template('dashboard.html', wishlist=wishlist)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8699, debug=False)
