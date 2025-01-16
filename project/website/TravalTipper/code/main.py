from flask import Flask, render_template, request, redirect, url_for, session, flash
from UserManager import UserManager
from TravelTipManager import TravelTipManager
from FavoritesManager import FavoritesManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'

user_manager = UserManager('users.txt')
travel_tip_manager = TravelTipManager('travel_tips.txt')
favorites_manager = FavoritesManager('favorites.txt')

@app.route('/')
def login_page():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    if user_manager.login(username, password):
        session['username'] = username
        return redirect(url_for('travel_tips_page'))
    flash('Invalid username or password. Please try again.')
    return redirect(url_for('login_page'))

@app.route('/register', methods=['GET', 'POST'])
def registration_page():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            flash('Registration successful! Please log in.')
            return redirect(url_for('login_page'))
        flash('Username already exists. Please choose another one.')
    return render_template('registration.html')

@app.route('/travel_tips', methods=['GET', 'POST'])
def travel_tips_page():
    if request.method == 'POST':
        destination = request.form['destination']
        trip_duration = request.form['trip_duration']
        interests = request.form.getlist('interests')
        recommendations = travel_tip_manager.generate_tips(destination, interests)
        return render_template('travel_tips.html', recommendations=recommendations)
    return render_template('travel_tips.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out.')
    return redirect(url_for('login_page'))

@app.route('/save_favorite', methods=['POST'])
def save_favorite():
    if 'username' in session:
        destination = request.form['destination']
        tip = travel_tip_manager.get_tip_by_destination(destination)
        if tip:
            favorites_manager.save_favorite(session['username'], tip)
            flash('Travel tip saved to favorites!')
        else:
            flash('Travel tip not found.')
    return redirect(url_for('travel_tips_page'))

@app.route('/view_favorites')
def view_favorites():
    if 'username' in session:
        favorites = favorites_manager.load_favorites(session['username'])
        return render_template('view_favorites.html', favorites=favorites)
    flash('You need to log in to view your favorites.')
    return redirect(url_for('login_page'))

@app.route('/search_tips', methods=['GET', 'POST'])
def search_tips():
    if request.method == 'POST':
        search_query = request.form['search_query']
        filtered_tips = travel_tip_manager.search_tips(search_query)
        return render_template('search_results.html', tips=filtered_tips)
    return render_template('search_tips.html')

if __name__ == '__main__':
    app.run(port=8664, debug=False)
