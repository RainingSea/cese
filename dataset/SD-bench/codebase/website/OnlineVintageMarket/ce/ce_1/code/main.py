from flask import Flask, render_template, request, redirect, url_for, session
from user_manager import UserManager
from item_manager import ItemManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'

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
        user_manager.add_user(username, password)
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/home', methods=['GET'])
def home():
    items = item_manager.get_all_items()
    return render_template('home.html', items=items)

@app.route('/item/<string:name>', methods=['GET'])
def item_details(name):
    item = item_manager.find_item(name)
    return render_template('item_details.html', item=item)

@app.route('/listing', methods=['GET', 'POST'])
def listing():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = float(request.form['price'])
        item_manager.add_item(name, description, price)
        return redirect(url_for('home'))
    return render_template('listing.html')

if __name__ == '__main__':
    user_manager.load_users()
    item_manager.load_items()
    app.run(port=8466, debug=False)
