from flask import Flask, render_template, request, redirect, session, url_for
from UserManager import UserManager
from PreferenceManager import PreferenceManager
from RecommendationEngine import RecommendationEngine
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key in production

user_manager = UserManager()
preference_manager = PreferenceManager()
recommendation_engine = RecommendationEngine()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.login(username, password):
            session['username'] = username
            return redirect('/preferences')
        else:
            return "Login Failed"
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            return redirect('/')
        else:
            return "Username already exists!"  # Updated error message
    return render_template('register.html')

@app.route('/preferences', methods=['GET', 'POST'])
def preferences():
    if 'username' not in session:
        return redirect('/')
    if request.method == 'POST':
        preferences = {
            'budget': request.form['budget'],
            'activities': request.form['activities'],
            'climate': request.form['climate']
        }
        preference_manager.save_preferences(session['username'], preferences)
        return redirect('/recommendations')
    return render_template('preferences.html')

@app.route('/recommendations')
def recommendations():
    if 'username' not in session:
        return redirect('/')
    preferences = preference_manager.load_preferences(session['username'])
    recommendations = recommendation_engine.generate_recommendations(preferences)
    return render_template('recommendations.html', recommendations=recommendations)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')

if __name__ == '__main__':
    user_manager.load_users()
    preference_manager.load_all_preferences()  # Updated to load all preferences
    app.run(port=8445, debug=False)
