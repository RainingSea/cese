from flask import Flask, render_template, request, redirect, url_for, session
from UserManager import UserManager
from ItemManager import ItemManager

app = Flask(__name__)
app.secret_key = 'supersecretkey'
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

@app.route('/home')
def home():
    return render_template('home.html', items=item_manager.load_items())

@app.route('/item/<name>')
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
    app.run(port=8316, debug=False)
