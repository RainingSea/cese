from flask import Flask, render_template, request, redirect, url_for, session
from user import User
from travel_tip import TravelTip
from favorites import Favorites

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def load_users():
    users = {}
    with open('users.txt', 'r') as file:
        for line in file:
            username, password = line.strip().split('|')
            users[username] = password
    return users

def load_tips():
    tips = {}
    with open('tips.txt', 'r') as file:
        for line in file:
            destination, duration, interests, tip = line.strip().split('|')
            if destination not in tips:
                tips[destination] = []
            tips[destination].append({'duration': duration, 'interests': interests.split(','), 'tip': tip})
    return tips

users = load_users()
tips = load_tips()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username not in users:
            new_user = User(username, password)
            new_user.save()
            users[username] = password
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    if username in users and users[username] == password:
        session['username'] = username
        return redirect(url_for('travel_details'))
    return redirect(url_for('login'))

@app.route('/travel_details', methods=['GET', 'POST'])
def travel_details():
    if request.method == 'POST':
        destination = request.form['destination']
        duration = request.form['duration']
        interests = request.form.getlist('interests')
        travel_tip = TravelTip(destination, duration, interests)
        recommendations = travel_tip.generate_tips()
        return render_template('recommendations.html', recommendations=recommendations)
    return render_template('travel_details.html')

@app.route('/favorites', methods=['GET', 'POST'])
def favorites():
    user_favorites = Favorites(session['username'])
    if request.method == 'POST':
        tip = request.form['tip']
        user_favorites.add_favorite(tip)
    return render_template('favorites.html', favorites=user_favorites.get_favorites())

if __name__ == '__main__':
    app.run(port=8663, debug=False)
