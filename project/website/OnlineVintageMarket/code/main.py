from flask import Flask, render_template, request, redirect, url_for, session
from auth_manager import AuthManager
from item_manager import ItemManager
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

auth_manager = AuthManager()
item_manager = ItemManager()

@app.route('/')
def login_route():
    if 'username' in session:
        return redirect(url_for('home_route'))
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_post():
    username = request.form['username']
    password = request.form['password']
    
    if auth_manager.login(username, password):
        session['username'] = username
        return redirect(url_for('home_route'))
    return render_template('login.html', error='Invalid credentials')

@app.route('/register', methods=['GET'])
def register_route():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register_post():
    username = request.form['username']
    password = request.form['password']
    email = request.form.get('email', '')
    
    if auth_manager.register(username, password, email):
        return redirect(url_for('login_route'))
    return render_template('register.html', error='Registration failed')

@app.route('/home')
def home_route():
    if 'username' not in session:
        return redirect(url_for('login_route'))
    
    query = request.args.get('query', '')
    items = item_manager.search_items(query) if query else item_manager.get_items()
    return render_template('home.html', items=items, username=session['username'])

@app.route('/listing', methods=['GET'])
def listing_route():
    if 'username' not in session:
        return redirect(url_for('login_route'))
    return render_template('listing.html')

@app.route('/listing', methods=['POST'])
def listing_post():
    if 'username' not in session:
        return redirect(url_for('login_route'))
    
    title = request.form['title']
    description = request.form['description']
    price = request.form['price']
    
    if item_manager.add_item(title, description, float(price), session['username']):
        return redirect(url_for('home_route'))
    return render_template('listing.html', error='Failed to add item')

@app.route('/item/<item_id>')
def item_details_route(item_id):
    if 'username' not in session:
        return redirect(url_for('login_route'))
    
    item = item_manager.get_item_details(item_id)
    if not item:
        return redirect(url_for('home_route'))
    return render_template('item_details.html', item=item)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login_route'))

if __name__ == '__main__':
    app.run(port=8120, debug=False)
