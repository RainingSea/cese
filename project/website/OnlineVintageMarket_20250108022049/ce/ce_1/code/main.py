from flask import Flask, render_template, request, redirect, url_for, session
from UserManager import UserManager
from ItemManager import ItemManager

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
    items = item_manager.load_items()
    return render_template('home.html', items=items)

@app.route('/item/<string:name>', methods=['GET'])
def item_details(name):
    item = item_manager.find_item(name)
    return render_template('item_details.html', item=item)

@app.route('/listing', methods=['GET'])
def listing():
    items = item_manager.load_items()
    return render_template('listing.html', items=items)

if __name__ == '__main__':
    app.run(port=8317, debug=False)
