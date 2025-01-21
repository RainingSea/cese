from flask import Flask, render_template, request, redirect, url_for, session
from user import User
from item import Item

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Load users and items from files
def load_users():
    users = []
    with open('users.txt', 'r') as file:
        for line in file:
            username, password = line.strip().split('|')
            users.append(User(username, password))
    return users

def load_items():
    items = []
    with open('items.txt', 'r') as file:
        for line in file:
            item_name, description, price = line.strip().split('|')
            items.append(Item(item_name, description, float(price)))
    return items

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        new_user = User(username, password)
        new_user.save()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/item/<item_id>')
def item_details(item_id):
    items = load_items()
    item = items[int(item_id)]
    return render_template('item_details.html', item=item)

@app.route('/listing', methods=['GET', 'POST'])
def listing():
    if request.method == 'POST':
        item_name = request.form['item_name']
        description = request.form['description']
        price = float(request.form['price'])
        new_item = Item(item_name, description, price)
        new_item.save()
        return redirect(url_for('home'))
    return render_template('listing.html')

if __name__ == '__main__':
    app.run(port=8965, debug=False)
