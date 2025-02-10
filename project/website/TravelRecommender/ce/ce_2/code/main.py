from flask import Flask, render_template, request, redirect, session
from user import User
from preferences import Preferences
from destination import Destination
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
        return redirect('/')

    return render_template('register.html')

@app.route('/preferences', methods=['GET', 'POST'])
def preferences():
    if request.method == 'POST':
        budget = float(request.form['budget'])
        activities = request.form.getlist('activities')
        climate = request.form['climate']
        preferences = Preferences(budget, activities, climate)
        preferences.save(session['username'])
        return redirect('/recommendations')

    return render_template('preferences.html')

@app.route('/recommendations')
def recommendations():
    destinations = Destination().load_all()
    return render_template('recommendations.html', destinations=destinations)

@app.route('/favorites')
def favorites():
    fav = Favorites(session['username'])
    favorite_destinations = fav.load(session['username'])
    return render_template('favorites.html', favorites=favorite_destinations)

if __name__ == '__main__':
    app.run(port=8673, debug=False)
