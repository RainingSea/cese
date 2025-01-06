from flask import Flask, render_template, request, redirect, url_for, session
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def register(self):
        users = self.load_all_users()
        if self.username in users:
            return False
        users[self.username] = self.password
        self.save(users)
        return True

    def login(self):
        users = self.load_all_users()
        return users.get(self.username) == self.password

    @staticmethod
    def load_all_users():
        try:
            with open('users.txt', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    @staticmethod
    def save(users):
        with open('users.txt', 'w') as f:
            json.dump(users, f)

class Item:
    def __init__(self, name, description, price):
        self.name = name
        self.description = description
        self.price = price

    @staticmethod
    def load_all():
        try:
            with open('items.txt', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    @staticmethod
    def save(item):
        items = Item.load_all()
        items.append(item.__dict__)
        with open('items.txt', 'w') as f:
            json.dump(items, f)

@app.route('/')
def login_page():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    user = User(username, password)
    if user.login():
        session['username'] = username
        return redirect(url_for('home'))
    return redirect(url_for('login_page'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User(username, password)
        if user.register():
            return redirect(url_for('login_page'))
    return render_template('register.html')

@app.route('/home')
def home():
    items = Item.load_all()
    return render_template('home.html', items=items)

@app.route('/item/<name>')
def item_details(name):
    items = Item.load_all()
    item = next((item for item in items if item['name'] == name), None)
    return render_template('item_details.html', item=item)

@app.route('/listing', methods=['GET', 'POST'])
def listing():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = float(request.form['price'])
        item = Item(name, description, price)
        Item.save(item)
        return redirect(url_for('home'))
    return render_template('listing.html')

if __name__ == '__main__':
    app.run(port=8179, debug=False)
