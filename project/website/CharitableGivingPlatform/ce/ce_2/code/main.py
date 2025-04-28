from flask import Flask, render_template, request, redirect, session
from user_manager import UserManager
from charity_manager import CharityManager
from contribution import Contribution

app = Flask(__name__)
app.secret_key = 'your_secret_key'

user_manager = UserManager()
charity_manager = CharityManager()
contribution_manager = Contribution()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    if user_manager.register(username, password):
        return redirect('/')
    return "Registration failed", 400

@app.route('/dashboard', methods=['POST'])
def dashboard():
    username = request.form['username']
    password = request.form['password']
    if user_manager.login(username, password):
        session['username'] = username
        return render_template('dashboard.html', charities=charity_manager.get_charities())
    return "Login failed", 400

@app.route('/charity/<charity_id>')
def charity_details(charity_id):
    charity_details = charity_manager.get_charity_details(charity_id)
    return render_template('charity_details.html', charity=charity_details)

@app.route('/donate', methods=['POST'])
def donate():
    charity_id = request.form['charity_id']
    amount = float(request.form['amount'])
    username = session.get('username')
    contribution_manager.add_contribution(username, charity_id, amount)
    return redirect('/dashboard')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')

if __name__ == '__main__':
    user_manager.load_users()
    charity_manager.load_charities()
    contribution_manager.load_contributions()
    app.run(port=8376, debug=False)
