from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'

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
        return redirect(url_for('login'))

    def login(self) -> str:
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            for user in self.users:
                if user.username == username and user.password == password:
                    session['username'] = username
                    return redirect(url_for('home'))
        return render_template('login.html')

    def register(self) -> str:
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            new_user = User(username, password)
            self.save_user({'username': new_user.username, 'password': new_user.password})
            return redirect(url_for('login'))
        return render_template('register.html')

    def home(self) -> str:
        return render_template('home.html', items=self.items)

    def listing(self) -> str:
        if request.method == 'POST':
            item_name = request.form['item_name']
            description = request.form['description']
            price = float(request.form['price'])
            new_item = Item(item_name, description, price)
            self.save_item({'item_name': new_item.item_name, 'description': new_item.description, 'price': new_item.price})
            return redirect(url_for('home'))
        return render_template('listing.html')

    def item_details(self, item_id: int) -> str:
        item = self.items[item_id]
        return render_template('item_details.html', item=item)

    def load_users(self) -> list:
        users = []
        if os.path.exists('users.txt'):
            with open('users.txt', 'r') as f:
                for line in f:
                    username, password = line.strip().split('|')
                    users.append(User(username, password))
        return users

    def load_items(self) -> list:
        items = []
        if os.path.exists('items.txt'):
            with open('items.txt', 'r') as f:
                for line in f:
                    item_name, description, price = line.strip().split('|')
                    items.append(Item(item_name, description, float(price)))
        return items

    def save_user(self, user_data: dict) -> None:
        with open('users.txt', 'a') as f:
            f.write(f"{user_data['username']}|{user_data['password']}\n")

    def save_item(self, item_data: dict) -> None:
        with open('items.txt', 'a') as f:
            f.write(f"{item_data['item_name']}|{item_data['description']}|{item_data['price']}\n")

main_app = Main()

@app.route('/')
def home():
    return main_app.login()

@app.route('/login', methods=['GET', 'POST'])
def login():
    return main_app.login()

@app.route('/register', methods=['GET', 'POST'])
def register():
    return main_app.register()

@app.route('/home')
def show_home():
    return main_app.home()

@app.route('/listing', methods=['GET', 'POST'])
def create_listing():
    return main_app.listing()

@app.route('/item/<int:item_id>')
def item_details(item_id):
    return main_app.item_details(item_id)

if __name__ == '__main__':
    app.run(port=8558, debug=False)
