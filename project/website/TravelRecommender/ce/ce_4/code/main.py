from flask import Flask, render_template, request, redirect, url_for, session
from user import User
from preferences import Preferences
from recommendations import Recommendations
from favorites import Favorites

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User(username, password)
        user.save()
        return redirect(url_for('login'))
    return render_template('registration.html')

@app.route('/preferences', methods=['GET', 'POST'])
def preferences():
    if request.method == 'POST':
        budget = float(request.form['budget'])
        activities = request.form.getlist('activities')
        climate = request.form['climate']
        prefs = Preferences(budget, activities, climate)
        prefs.save()
        return redirect(url_for('recommendations'))
    return render_template('preferences.html')

@app.route('/recommendations')
def recommendations():
    prefs = Preferences.load()
    recommender = Recommendations()
    destinations = recommender.generate(prefs)
    return render_template('recommendations.html', destinations=destinations)

@app.route('/favorites')
def favorites():
    favs = Favorites()
    favorite_destinations = favs.load()
    return render_template('favorites.html', favorites=favorite_destinations)

if __name__ == '__main__':
    app.run(port=8675, debug=False)
