from flask import Flask, render_template, request, redirect, url_for, flash
from user_manager import UserManager
from travel_tip_manager import TravelTipManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key

user_manager = UserManager('users.txt')
travel_tip_manager = TravelTipManager('travel_tips.txt')

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            flash('Registration successful! Please log in.')
            return redirect(url_for('login'))
        else:
            flash('Username already exists. Please choose a different one.')
    return render_template('registration.html')

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    if user_manager.login(username, password):
        flash('Login successful!')
        return redirect(url_for('travel_tips'))
    else:
        flash('Invalid username or password. Please try again.')
        return redirect(url_for('login'))

@app.route('/travel_tips', methods=['GET', 'POST'])
def travel_tips():
    if request.method == 'POST':
        destination = request.form['destination']
        tips = request.form['tips']
        travel_tip_manager.add_tip(destination, tips)
        flash('Travel tip added successfully!')
    tips = travel_tip_manager.get_tips('default')  # Example for default destination
    return render_template('travel_tips.html', tips=tips)

if __name__ == '__main__':
    app.run(port=8662, debug=False)
