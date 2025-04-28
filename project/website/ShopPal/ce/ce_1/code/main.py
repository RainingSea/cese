from flask import Flask, render_template, request, redirect, url_for
from user_manager import UserManager
from product_manager import ProductManager
from collection_manager import CollectionManager

app = Flask(__name__)

user_manager = UserManager()
product_manager = ProductManager()
collection_manager = CollectionManager()

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

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if request.method == 'POST':
        username = request.form['username']
        product_id = request.form['product_id']
        collection_manager.add_to_collection(username, product_id)
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run(port=8411, debug=False)
