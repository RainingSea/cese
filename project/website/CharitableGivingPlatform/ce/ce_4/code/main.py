from flask import Flask, render_template, request, redirect, url_for, session
from user import User
from charity import Charity
from donation import Donation

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def load_users():
    users = User.load_all()
    return {user.username: user.password for user in users}

def load_charities():
    charities = Charity.load_all()
    return charities

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
    users = load_users()
    charities = load_charities()
    return render_template('dashboard.html', charities=charities)

@app.route('/charity/<charity_name>', methods=['GET'])
def charity_details(charity_name):
    charities = load_charities()
    charity = next((c for c in charities if c.name == charity_name), None)
    return render_template('charity_details.html', charity=charity)

@app.route('/donate', methods=['POST'])
def donate():
    username = request.form['username']
    charity_name = request.form['charity_name']
    amount = float(request.form['amount'])
    donation = Donation(username, charity_name, amount)
    donation.save()
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(port=8597, debug=False)
