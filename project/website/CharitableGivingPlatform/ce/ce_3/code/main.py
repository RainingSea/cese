from flask import Flask, render_template, request, redirect, url_for, session
from user import User
from charity import Charity
from donation import Donation

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Load users, charities, and donations from files
def load_data():
    users = User.load_all()
    charities = Charity.load_all()
    donations = Donation.load_all()
    return users, charities, donations

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
    users, charities, donations = load_data()
    return render_template('dashboard.html', charities=charities, donations=donations)

@app.route('/charity/<charity_name>')
def charity_details(charity_name):
    charities = Charity.load_all()
    charity = next((c for c in charities if c.name == charity_name), None)
    return render_template('charity_details.html', charity=charity)

if __name__ == '__main__':
    app.run(port=9001, debug=False)
