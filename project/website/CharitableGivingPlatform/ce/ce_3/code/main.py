from flask import Flask, render_template, request, redirect, url_for
from user import User
from charity import Charity
from donation import Donation

app = Flask(__name__)

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

@app.route('/dashboard')
def dashboard():
    users = User.load_all()
    charities = Charity.load_all()
    return render_template('dashboard.html', users=users, charities=charities)

@app.route('/charity/<charity_name>')
def charity_details(charity_name):
    charity = Charity.load_all()
    charity_info = next((c for c in charity if c.name == charity_name), None)
    return render_template('charity_details.html', charity=charity_info)

if __name__ == '__main__':
    app.run(port=8596, debug=False)
