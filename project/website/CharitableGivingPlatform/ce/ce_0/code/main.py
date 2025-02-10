from flask import Flask, render_template, request, redirect, url_for, session
from user import User
from charity import Charity
from contribution import Contribution

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Load users, charities, and contributions from files
users = User.load_users()
charities = Charity.load_charities()
contributions = Contribution.load_contributions()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        new_user = User(username, password)
        new_user.save()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/dashboard', methods=['GET'])
def dashboard():
    return render_template('dashboard.html', charities=charities, contributions=contributions)

@app.route('/charity/<charity_name>', methods=['GET'])
def charity_details(charity_name):
    charity = next((c for c in charities if c.name == charity_name), None)
    return render_template('charity_details.html', charity=charity)

if __name__ == '__main__':
    app.run(port=8593, debug=False)
