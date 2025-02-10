from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

class Item:
    def __init__(self, item_name: str, description: str, price: float):
        self.item_name = item_name
        self.description = description
        self.price = price

class Main:
    def __init__(self):
        self.users = self.load_users()
        self.items = self.load_items()

    def main(self) -> str:
        return "Welcome to the Vintage Items App!"

    def login(self) -> str:
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            if username in self.users and self.users[username] == password:
                return redirect(url_for('home'))
        return render_template('login.html')

    def register(self) -> str:
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            self.save_user(username, password)
            return redirect(url_for('login'))
        return render_template('register.html')

    def home(self) -> str:
        return render_template('home.html', items=self.items)

    def listing(self) -> str:
        if request.method == 'POST':
            item_name = request.form['item_name']
            description = request.form['description']
            price = float(request.form['price'])
            self.submit_listing(item_name, description, price)
            return redirect(url_for('home'))
        return render_template('listing.html')

    def item_details(self, item_id: str) -> str:
        item = self.items[int(item_id)]
        return render_template('item_details.html', item=item)

    def submit_listing(self, item_name: str, description: str, price: float) -> None:
        self.save_item(item_name, description, price)

    def load_users(self) -> dict:
        users = {}
        if os.path.exists('users.txt'):
            with open('users.txt', 'r') as file:
                for line in file:
                    username, password = line.strip().split('|')
                    users[username] = password
        return users

    def load_items(self) -> list:
        items = []
        if os.path.exists('items.txt'):
            with open('items.txt', 'r') as file:
                for line in file:
                    item_name, description, price = line.strip().split('|')
                    items.append(Item(item_name, description, float(price)))
        return items

    def save_user(self, username: str, password: str) -> None:
        with open('users.txt', 'a') as file:
            file.write(f"{username}|{password}\n")
        self.users[username] = password

    def save_item(self, item_name: str, description: str, price: float) -> None:
        with open('items.txt', 'a') as file:
            file.write(f"{item_name}|{description}|{price}\n")
        self.items.append(Item(item_name, description, price))

main_app = Main()

@app.route('/', methods=['GET', 'POST'])
def login():
    return main_app.login()

@app.route('/register', methods=['GET', 'POST'])
def register():
    return main_app.register()

@app.route('/home')
def home():
    return main_app.home()

@app.route('/listing', methods=['GET', 'POST'])
def listing():
    return main_app.listing()

@app.route('/item_details/<item_id>')
def item_details(item_id):
    return main_app.item_details(item_id)

if __name__ == '__main__':
    app.run(port=8560, debug=False)
