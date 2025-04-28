from flask import Flask, render_template, request, redirect, url_for, session
from user_manager import UserManager
from item_manager import ItemManager
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key

user_manager = UserManager()
item_manager = ItemManager()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            return redirect(url_for('login'))
    return render_template('registration.html')

@app.route('/home', methods=['GET'])
def home():
    items = item_manager.get_items()
    return render_template('home.html', items=items)

@app.route('/listing', methods=['GET', 'POST'])
def listing():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = float(request.form['price'])
        item_manager.add_item(name, description, price)
        return redirect(url_for('home'))
    return render_template('listing.html')

@app.route('/item/<name>', methods=['GET'])
def item_details(name):
    details = item_manager.get_item_details(name)
    return render_template('item_details.html', details=details)

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    if user_manager.login(username, password):
        return redirect(url_for('home'))
    return redirect(url_for('login'))

if __name__ == '__main__':
    user_manager.load_users()
    item_manager.load_items()
    app.run(port=8380, debug=False)
