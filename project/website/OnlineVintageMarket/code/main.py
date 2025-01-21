from flask import Flask, render_template, request, redirect, session
from user import User
from item import Item
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Load users and items from files
def load_users() -> list:
    """Load users from the users.txt file."""
    users = []
    if not os.path.exists('users.txt'):
        print("Warning: users.txt file not found. Starting with an empty user list.")
        return users
    
    with open('users.txt', 'r') as file:
        for line in file:
            username, password = line.strip().split('|')
            users.append(User(username, password))
    return users

def load_items() -> list:
    """Load items from the items.txt file."""
    items = []
    if not os.path.exists('items.txt'):
        print("Warning: items.txt file not found. Starting with an empty item list.")
        return items
    
    with open('items.txt', 'r') as file:
        for line in file:
            name, description, price = line.strip().split('|')
            items.append(Item(name, description, float(price)))
    return items

users = load_users()
items = load_items()

@app.route('/')
def login():
    """Render the login page."""
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Handle user registration."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if register_user(username, password):
            return redirect('/')
    return render_template('registration.html')

def register_user(username: str, password: str) -> bool:
    """Register a new user if the username is not taken."""
    if any(user.username == username for user in users):
        return False
    new_user = User(username, password)
    users.append(new_user)
    save_users()
    return True

def save_users() -> None:
    """Save users to the users.txt file."""
    with open('users.txt', 'w') as file:
        for user in users:
            file.write(f"{user.username}|{user.password}\n")

@app.route('/home')
def home():
    """Render the home page with available items."""
    if not items:
        return "No vintage items found."
    return render_template('home.html', items=items)

@app.route('/listing', methods=['GET', 'POST'])
def listing():
    """Handle item listing."""
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = float(request.form['price'])
        if add_item(name, description, price):
            return redirect('/home')
        else:
            return "Error: Item listing failed."
    return render_template('listing.html')

def add_item(name: str, description: str, price: float) -> bool:
    """Add a new item and save it to the items file."""
    if any(item.name == name for item in items):
        return False
    new_item = Item(name, description, price)
    items.append(new_item)
    save_items()
    return True

def save_items() -> None:
    """Save items to the items.txt file."""
    with open('items.txt', 'w') as file:
        for item in items:
            file.write(f"{item.name}|{item.description}|{item.price}\n")

@app.route('/item/<name>')
def item_details(name: str):
    """Render the details of a specific item."""
    item = next((item for item in items if item.name == name), None)
    if item is None:
        return "Item not found."
    return render_template('item_details.html', item=item)

@app.route('/login', methods=['POST'])
def handle_login():
    """Handle user login."""
    username = request.form['username']
    password = request.form['password']
    for user in users:
        if user.username == username and user.password == password:
            session['username'] = username
            return redirect('/home')
    return redirect('/')

@app.route('/search', methods=['GET'])
def search_for_specific_vintage_item():
    """Search for a specific vintage item."""
    query = request.args.get('query')
    filtered_items = [item for item in items if query.lower() in item.name.lower()]
    return render_template('search_results.html', items=filtered_items)

if __name__ == '__main__':
    app.run(port=8967, debug=False)
