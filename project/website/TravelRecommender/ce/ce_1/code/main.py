from flask import Flask, render_template, request, redirect, url_for, session
from user import User
from preferences import Preferences
from destination import Destination
from recommendation_engine import RecommendationEngine

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this in production

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
    return render_template('register.html')

@app.route('/preferences', methods=['GET', 'POST'])
def preferences():
    if request.method == 'POST':
        budget = float(request.form['budget'])
        activities = request.form.getlist('activities')
        climate = request.form['climate']
        preferences = Preferences(budget, activities, climate)
        preferences.save_preferences()
        return redirect(url_for('recommendations'))
    return render_template('preferences.html')

@app.route('/recommendations')
def recommendations():
    preferences = Preferences.load_preferences()[-1]  # Load last saved preferences
    recommendation_engine = RecommendationEngine()
    recommendations = recommendation_engine.generate_recommendations(preferences)
    return render_template('recommendations.html', recommendations=recommendations)

if __name__ == '__main__':
    app.run(port=8672, debug=False)
