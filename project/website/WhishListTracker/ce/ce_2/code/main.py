from flask import Flask, render_template, request, redirect, session, url_for
from user import User
from wishlist_item import WishlistItem

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User(username, password)
        user.save()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        item_name = request.form['name']
        item_description = request.form['description']
        item_price = float(request.form['price'])
        wishlist_item = WishlistItem(item_name, item_description, item_price)
        wishlist_item.save()
    
    wishlist_items = WishlistItem.load_all()
    return render_template('dashboard.html', items=wishlist_items)

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    users = User.load_all()
    
    for user in users:
        if user.username == username and user.password == password:
            session['username'] = username
            return redirect(url_for('dashboard'))
    
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8700, debug=False)
