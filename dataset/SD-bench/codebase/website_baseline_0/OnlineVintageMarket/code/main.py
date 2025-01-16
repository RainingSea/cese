from flask import Flask, render_template, request, redirect, url_for, session
from user import User
from item import Item

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Load users and items from files
def load_users():
    return User.load_users()

def load_items():
    return Item.load_items()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def user_login():
    username = request.form['username']
    password = request.form['password']
    users = load_users()
    user = next((user for user in users if user.username == username and user.password == password), None)
    if user:
        session['username'] = username
        return redirect(url_for('home'))
    return "Invalid credentials", 401

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User(username, password)
        user.save()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/home')
def home():
    items = load_items()
    return render_template('home.html', items=items)

@app.route('/listing', methods=['GET', 'POST'])
def listing():
    if request.method == 'POST':
        item_id = len(load_items()) + 1
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']
        item = Item(item_id, name, description, float(price))
        item.save()
        return redirect(url_for('home'))
    return render_template('listing.html')

@app.route('/item/<int:item_id>')
def item_details(item_id):
    items = load_items()
    item = next((item for item in items if item.item_id == item_id), None)
    return render_template('item_details.html', item=item)

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    items = load_items()
    filtered_items = [item for item in items if query.lower() in item.name.lower()]
    return render_template('home.html', items=filtered_items)

@app.route('/navigate_back')
def navigate_back():
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(port=8545, debug=False)
