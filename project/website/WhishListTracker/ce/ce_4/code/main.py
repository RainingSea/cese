from flask import Flask, render_template, request, redirect, session
from user import User
from auth import Auth
from dashboard import Dashboard
from wishlist_item import WishlistItem

app = Flask(__name__)
app.secret_key = 'your_secret_key'

auth = Auth()
dashboard = Dashboard()

@app.route('/')
def login_page():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    if auth.login(username, password):
        session['username'] = username
        return redirect('/dashboard')
    return redirect('/')

@app.route('/register')
def register_page():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    if auth.register(username, password):
        return redirect('/')
    return redirect('/register')

@app.route('/dashboard')
def dashboard_page():
    if 'username' not in session:
        return redirect('/')
    items = dashboard.view_items()
    return render_template('dashboard.html', items=items)

@app.route('/add_item', methods=['POST'])
def add_item():
    name = request.form['name']
    description = request.form['description']
    price = float(request.form['price'])
    dashboard.add_item(name, description, price)
    return redirect('/dashboard')

@app.route('/logout')
def logout():
    auth.logout()
    return redirect('/')

if __name__ == '__main__':
    app.run(port=8702, debug=False)
