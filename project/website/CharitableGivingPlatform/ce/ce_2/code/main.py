from flask import Flask, render_template, request, redirect, url_for, session
from user import User
from charity import Charity
from donation import Donation

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Load users, charities, and donations from files
users = User().load_users()
charities = Charity().load_charities()
donations = Donation().load_donations()

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

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', charities=charities, donations=donations)

@app.route('/charity/<name>')
def charity_details(name):
    charity = next((c for c in charities if c.name == name), None)
    return render_template('charity_details.html', charity=charity)

@app.route('/donate', methods=['POST'])
def donate():
    username = session.get('username')
    charity_name = request.form['charity_name']
    amount = float(request.form['amount'])
    donation = Donation(username, charity_name, amount)
    donation.save_donation()
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(port=9000, debug=False)
