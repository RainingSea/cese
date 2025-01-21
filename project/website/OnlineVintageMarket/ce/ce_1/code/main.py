from flask import Flask, render_template, request, redirect, url_for, session
from user import User
from item import Item

app = Flask(__name__)
app.secret_key = 'your_secret_key'
users = User().load_all()
items = Item().load_all()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        User(username, password).save()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/home')
def home():
    return render_template('home.html', items=items)

@app.route('/item/<name>')
def item_details(name):
    item = Item().get_item_details(name)
    return render_template('item_details.html', item=item)

@app.route('/listing', methods=['GET', 'POST'])
def listing():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = float(request.form['price'])
        Item(name, description, price).save()
        return redirect(url_for('home'))
    return render_template('listing.html')

if __name__ == '__main__':
    app.run(port=8963, debug=False)
