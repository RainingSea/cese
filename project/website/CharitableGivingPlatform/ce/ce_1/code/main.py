from flask import Flask, render_template, request, redirect, session
from models import User, Charity, Donation
from data_storage import user_storage, charity_storage, donation_storage

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
        if user_storage.get_user(username) is None:
            new_user = User(username, password)
            user_storage.save_user(new_user)
            return redirect('/')
    return render_template('register.html')


@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        charities = charity_storage.load_charities()
        user_donations = donation_storage.get_user_donations(session['username'])
        return render_template('dashboard.html', charities=charities, donations=user_donations)
    return redirect('/')


@app.route('/charity/<charity_name>')
def charity_details(charity_name):
    charity = charity_storage.get_charity(charity_name)
    return render_template('charity_details.html', charity=charity)


@app.route('/login', methods=['POST'])
def login_user():
    username = request.form['username']
    password = request.form['password']
    user = user_storage.get_user(username)
    if user and user.password == password:
        session['username'] = user.username
        return redirect('/dashboard')
    return redirect('/')


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')


if __name__ == '__main__':
    app.run(port=8329, debug=False)
