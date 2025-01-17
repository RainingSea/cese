from flask import Flask, render_template, request, redirect, url_for, flash, session
from user import User
from charity import Charity
from donation import Donation
from data_manager import DataManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for flash messages
data_manager = DataManager()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = data_manager.load_users()
        for user in users:
            if user.username == username and user.password == password:
                session['username'] = username  # Store username in session
                return redirect(url_for('dashboard'))
        flash('Invalid username or password')  # Flash message for invalid login
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
    charities = data_manager.load_charities()
    if not charities:
        flash('No charities found. Please add some charities.')  # Flash message for no charities
    return render_template('dashboard.html', charities=charities)

@app.route('/charity/<charity_name>', methods=['GET', 'POST'])
def charity_details(charity_name):
    charities = data_manager.load_charities()
    charity = next((c for c in charities if c.name == charity_name), None)
    if charity:
        if request.method == 'POST':
            try:
                donation_amount = float(request.form['amount'])
                if donation_amount <= 0:
                    flash('Donation amount must be greater than zero.')  # Flash message for invalid donation
                    return redirect(url_for('charity_details', charity_name=charity_name))
                donation = Donation(user=session.get('username'), charity=charity_name, amount=donation_amount, date='2023-10-03')
                data_manager.save_donations([donation])
                return redirect(url_for('dashboard'))
            except ValueError:
                flash('Invalid donation amount. Please enter a numeric value.')  # Flash message for invalid input
                return redirect(url_for('charity_details', charity_name=charity_name))
        return render_template('charity_details.html', charity=charity)
    flash('Charity not found.')  # Flash message for charity not found
    return redirect(url_for('dashboard'))

@app.route('/logout')
def logout():
    session.pop('username', None)  # Remove username from session
    flash('You have been logged out.')  # Flash message for logout
    return redirect(url_for('login'))

@app.route('/view_contribution_history')
def view_contribution_history():
    username = session.get('username')
    if not username:
        flash('You need to log in to view your contribution history.')
        return redirect(url_for('login'))
    
    users = data_manager.load_users()
    user = next((u for u in users if u.username == username), None)
    if user:
        contributions = user.get_contribution_history()
        return render_template('contribution_history.html', contributions=contributions)
    
    flash('No contributions found.')
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(port=8760, debug=False)
