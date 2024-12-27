from flask import Flask, render_template, request, redirect, url_for, flash
from data_storage import DataStorage, User, Charity, Donation

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure key in production

data_storage = DataStorage()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username and password:
            new_user = User(username, password)
            data_storage.save_user(new_user)
            flash('Registration successful! You can now log in.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Please enter both username and password.', 'error')
    return render_template('register.html')

@app.route('/dashboard', methods=['POST'])
def dashboard():
    username = request.form['username']
    password = request.form['password']
    users = data_storage.load_users()
    for user in users:
        if user.username == username and user.password == password:
            charities = data_storage.load_charities()
            contributions = user.get_contributions()
            return render_template('dashboard.html', username=username, charities=charities, contributions=contributions)
    flash('Invalid username or password. Please try again.', 'error')
    return redirect(url_for('login'))

@app.route('/charity/<charity_name>', methods=['GET', 'POST'])
def charity_details(charity_name):
    charities = data_storage.load_charities()
    charity = next((c for c in charities if c.name == charity_name), None)
    if charity:
        if request.method == 'POST':
            amount = float(request.form['amount'])
            username = request.form['username']
            donation = Donation(username, charity_name, amount)
            data_storage.save_donation(donation)
            user = next((u for u in data_storage.load_users() if u.username == username), None)
            if user:
                user.add_contribution(amount)
            flash('Donation successful!', 'success')
            return redirect(url_for('dashboard'))
        return render_template('charity_details.html', charity=charity)
    flash('Charity not found.', 'error')
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True)