from flask import Flask, render_template, request, redirect, url_for, session
from user_manager import UserManager
from travel_tip_manager import TravelTipManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'
user_manager = UserManager()
travel_tip_manager = TravelTipManager()

user_manager.load_users('users.txt')
travel_tip_manager.load_tips('tips.txt')

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_manager.register_user(username, password)
        return redirect(url_for('login'))
    return render_template('registration.html')

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    if user_manager.login_user(username, password):
        session['username'] = username
        return redirect(url_for('input_travel_details'))
    return redirect(url_for('login'))

@app.route('/travel_details', methods=['GET', 'POST'])
def input_travel_details():
    if request.method == 'POST':
        destination = request.form['destination']
        trip_duration = request.form['trip_duration']
        interests = request.form.getlist('interests')
        recommendations = travel_tip_manager.get_tips(destination, interests)
        return render_template('recommendations.html', recommendations=recommendations)
    return render_template('travel_details.html')

@app.route('/favorites')
def favorites():
    return render_template('favorites.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8659, debug=False)
