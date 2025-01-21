from flask import Flask, render_template, request, redirect, url_for, session
from user import User
from item import Item
from auth import Auth
from listing import Listing

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Load users and items from files
users = User().load_users()
items = Item().load_items()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        Auth().register(username, password)
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/home')
def home():
    return render_template('home.html', items=items)

@app.route('/listing', methods=['GET', 'POST'])
def listing():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = float(request.form['price'])
        Listing().create_listing(name, description, price)
        return redirect(url_for('home'))
    return render_template('listing.html')

@app.route('/item/<int:item_id>')
def item_details(item_id):
    item = items[item_id]
    return render_template('item_details.html', item=item)

if __name__ == '__main__':
    app.run(port=8966, debug=False)
