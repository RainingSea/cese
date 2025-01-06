from flask import Flask, render_template, request, redirect, session
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def register(self):
        users = self.load_users()
        if self.username not in users:
            users[self.username] = self.password
            self.save_users(users)
            return True
        return False

    def login(self):
        users = self.load_users()
        return users.get(self.username) == self.password

    @staticmethod
    def load_users():
        try:
            with open('users.txt', 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    @staticmethod
    def save_users(users):
        with open('users.txt', 'w') as file:
            json.dump(users, file)

class Item:
    def __init__(self, name, description, price):
        self.name = name
        self.description = description
        self.price = price

    @staticmethod
    def load_all():
        try:
            with open('items.txt', 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return []

    @staticmethod
    def save(items):
        with open('items.txt', 'w') as file:
            json.dump(items, file)

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User(username, password)
        if user.login():
            session['username'] = username
            return redirect('/home')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User(username, password)
        if user.register():
            return redirect('/')
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
        items = Item.load_all()
        items.append({'name': name, 'description': description, 'price': price})
        Item.save(items)
        return redirect('/home')
    return render_template('listing.html')

if __name__ == '__main__':
    app.run(port=8180, debug=False)
