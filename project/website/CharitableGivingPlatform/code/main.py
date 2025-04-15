from flask import Flask, render_template, request, redirect, url_for, session
from data_storage import DataStorage
from models import User, Charity, Donation
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session management
data_storage = DataStorage()

@app.route('/', methods=['GET', 'POST'])
def login():
    """Handle user login."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = data_storage.load_users()
        for user in users:
            if user.username == username and user.password == password:
                session['username'] = username  # Store username in session
                return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Handle user registration."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if register_user(username, password):
            return redirect(url_for('login'))
    return render_template('register.html')

def register_user(username: str, password: str) -> bool:
    """Register a new user."""
    users = data_storage.load_users()
    for user in users:
        if user.username == username:
            return False
    new_user = User(username, password)
    users.append(new_user)
    data_storage.save_users(users)
    return True

@app.route('/dashboard')
def dashboard():
    """Display the dashboard with a list of charities and user donations."""
    if 'username' in session:
        charities = data_storage.load_charities()
        user_donations = data_storage.load_donations()
        return render_template('dashboard.html', charities=charities, donations=user_donations)
    return redirect(url_for('login'))

@app.route('/charity/<charity_name>', methods=['GET', 'POST'])
def charity_details(charity_name):
    """Display details of a specific charity and handle donations."""
    charities = data_storage.load_charities()
    for charity in charities:
        if charity.name == charity_name:
            if request.method == 'POST':
                amount = float(request.form['amount'])
                date = datetime.now().strftime('%Y-%m-%d')
                username = session['username']
                donation = Donation(data_storage.get_user_by_username(username), charity, amount, date)
                donation.user.add_contribution(amount)  # Update user's contribution history
                donations = data_storage.load_donations()
                donations.append(donation)
                data_storage.save_donations(donations)
                return redirect(url_for('dashboard'))
            return render_template('charity_details.html', charity=charity.get_details())
    return redirect(url_for('dashboard'))

@app.route('/logout')
def logout():
    """Handle user logout."""
    session.pop('username', None)  # Remove username from session
    return redirect(url_for('login'))

@app.route('/contribution_history')
def contribution_history():
    """Display the user's contribution history."""
    if 'username' in session:
        user = data_storage.get_user_by_username(session['username'])
        return render_template('contribution_history.html', contributions=user.get_contribution_history())
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8332, debug=False)
