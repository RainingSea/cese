from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def register(self, username: str, password: str) -> bool:
        with open('users.txt', 'a') as f:
            f.write(f"{username}|{password}\n")
        return True

    def login(self, username: str, password: str) -> bool:
        with open('users.txt', 'r') as f:
            for line in f:
                user_data = line.strip().split('|')
                if user_data[0] == username and user_data[1] == password:
                    return True
        return False

class WishlistItem:
    def __init__(self):
        self.items = self.load_items()

    def load_items(self):
        items = []
        if os.path.exists('wishlist.txt'):
            with open('wishlist.txt', 'r') as f:
                for line in f:
                    item_data = line.strip().split('|')
                    items.append({
                        'name': item_data[0],
                        'description': item_data[1],
                        'price': float(item_data[2])
                    })
        return items

    def add_item(self, name: str, description: str, price: float) -> bool:
        with open('wishlist.txt', 'a') as f:
            f.write(f"{name}|{description}|{price}\n")
        self.items.append({'name': name, 'description': description, 'price': price})
        return True

    def update_item(self, name: str, description: str, price: float) -> bool:
        updated = False
        for item in self.items:
            if item['name'] == name:
                item['description'] = description
                item['price'] = price
                updated = True
                break
        if updated:
            self.save_items()
        return updated

    def remove_item(self, name: str) -> bool:
        self.items = [item for item in self.items if item['name'] != name]
        self.save_items()
        return True

    def save_items(self):
        with open('wishlist.txt', 'w') as f:
            for item in self.items:
                f.write(f"{item['name']}|{item['description']}|{item['price']}\n")

@app.route('/')
def login_page():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    user = User(username, password)
    if user.login(username, password):
        session['username'] = username
        return redirect(url_for('dashboard'))
    return redirect(url_for('login_page'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User(username, password)
        user.register(username, password)
        return redirect(url_for('login_page'))
    return render_template('registration.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login_page'))
    wishlist = WishlistItem()
    return render_template('dashboard.html', items=wishlist.items)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login_page'))

if __name__ == '__main__':
    app.run(port=8287, debug=False)
