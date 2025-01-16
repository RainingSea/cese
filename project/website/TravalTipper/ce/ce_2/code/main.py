from flask import Flask, render_template, request, redirect, url_for, session
from UserManager import UserManager
from TravelTipManager import TravelTipManager

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Replace with a strong secret key

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
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    if user_manager.login(username, password):
        session['username'] = username
        return redirect(url_for('travel_details'))
    return redirect(url_for('login'))

@app.route('/travel_details', methods=['GET', 'POST'])
def travel_details():
    if request.method == 'POST':
        destination = request.form['destination']
        interests = request.form.getlist('interests')
        tips = travel_tip_manager.get_tips(destination, interests)
        return render_template('recommendations.html', tips=tips)
    return render_template('travel_details.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8661, debug=False)
