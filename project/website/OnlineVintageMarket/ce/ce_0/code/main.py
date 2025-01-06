from flask import Flask, render_template, request, redirect, session
from user import User
from item import Item

app = Flask(__name__)
app.secret_key = 'your_secret_key'
users = []
items = []

def load_users():
    global users
    try:
        with open('users.txt', 'r') as file:
            users = [User(*line.strip().split('|')) for line in file.readlines()]
    except FileNotFoundError:
        users = []

def load_items():
    global items
    try:
        with open('items.txt', 'r') as file:
            items = [Item(*line.strip().split('|')) for line in file.readlines()]
    except FileNotFoundError:
        items = []

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
        return redirect('/home')
    return redirect('/')

@app.route('/register')
def register_page():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    user = User(username, password)
    if user.register():
        return redirect('/')
    return redirect('/register')

@app.route('/home')
def home_page():
    load_items()
    return render_template('home.html', items=items)

@app.route('/item/<name>')
def item_details(name):
    item = next((item for item in items if item.name == name), None)
    return render_template('item_details.html', item=item)

@app.route('/listing')
def listing_page():
    return render_template('listing.html')

@app.route('/listing', methods=['POST'])
def create_listing():
    name = request.form['name']
    description = request.form['description']
    price = float(request.form['price'])
    item = Item(name, description, price)
    item.save()
    return redirect('/home')

if __name__ == '__main__':
    load_users()
    load_items()
    app.run(port=8178, debug=False)
