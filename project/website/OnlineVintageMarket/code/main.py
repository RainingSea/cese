from flask import Flask, render_template, request, redirect, url_for, session
from user import User
from item import Item

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Load users and items from files
def load_users():
    users = []
    try:
        with open('users.txt', 'r') as f:
            for line in f:
                username, password = line.strip().split('|')
                users.append(User(username, password))
    except FileNotFoundError:
        pass
    return users

def load_items():
    items = []
    try:
        with open('items.txt', 'r') as f:
            for line in f:
                name, description, price = line.strip().split('|')
                items.append(Item(name, description, float(price)))
    except FileNotFoundError:
        pass
    return items

users = load_users()
items = load_items()

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
    return render_template('home.html', items=items)

@app.route('/item/<name>')
def item_details(name):
    item = next((item for item in items if item.name == name), None)
    return render_template('item_details.html', item=item)

@app.route('/listing', methods=['GET', 'POST'])
def listing():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = float(request.form['price'])
        item = Item(name, description, price)
        items.append(item)
        with open('items.txt', 'a') as f:
            f.write(f"{name}|{description}|{price}\n")
        return redirect(url_for('home'))
    return render_template('listing.html')

if __name__ == '__main__':
    app.run(port=8181, debug=False)
