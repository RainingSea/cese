from flask import Flask, render_template, request, redirect, url_for, flash
from UserManager import UserManager
from ItemManager import ItemManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'

user_manager = UserManager()
item_manager = ItemManager()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = user_manager.find_user(username)
        if user and user.password == password:
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password.')
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
    return render_template('home.html')

@app.route('/items/<name>')
def item_details(name):
    item = item_manager.find_item(name)
    return render_template('item_details.html', item=item)

@app.route('/listing', methods=['GET'])
def listing():
    items = item_manager.load_items()
    return render_template('listing.html', items=items)

if __name__ == '__main__':
    user_manager.load_users()
    item_manager.load_items()
    app.run(port=8319, debug=False)
