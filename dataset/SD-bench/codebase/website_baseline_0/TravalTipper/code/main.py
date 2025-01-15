from flask import Flask, render_template, request, redirect, url_for, session
from user_manager import UserManager
from travel_tip_manager import TravelTipManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'

user_manager = UserManager()
tip_manager = TravelTipManager()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.is_username_taken(username):
            return render_template('register.html', error="Username already exists.")
        user_manager.register(username, password)
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
        duration = request.form['duration']
        interests = request.form.getlist('interests')
        tips = tip_manager.load_tips()
        generated_tips = [tip.generate_tips()[0] for tip in tips if tip.destination == destination]
        return render_template('recommendations.html', tips=generated_tips)
    return render_template('travel_details.html')

@app.route('/favorites', methods=['GET', 'POST'])
def favorites():
    if request.method == 'POST':
        tip = request.form['tip']
        user_manager.save_favorite(session['username'], tip)
    favorites = user_manager.get_favorites(session['username'])
    return render_template('favorites.html', favorites=favorites)

@app.route('/view_saved_travel_tips')
def view_saved_travel_tips():
    favorites = user_manager.get_favorites(session['username'])
    return render_template('favorites.html', favorites=favorites)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8558, debug=False)
