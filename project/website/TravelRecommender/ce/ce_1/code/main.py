from flask import Flask, render_template, request, redirect, url_for
from tools import UserManager, RecommendationEngine

app = Flask(__name__)
user_manager = UserManager()
recommendation_engine = RecommendationEngine()

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
    return render_template('registration.html')

@app.route('/preferences', methods=['GET', 'POST'])
def preferences():
    if request.method == 'POST':
        budget = request.form['budget']
        activities = request.form['activities']
        climate = request.form['climate']
        preferences = {'budget': budget, 'activities': activities, 'climate': climate}
        recommendations = recommendation_engine.generate_recommendations(preferences)
        return render_template('recommendations.html', recommendations=recommendations)
    return render_template('preferences.html')

@app.route('/favorites')
def favorites():
    return render_template('favorites.html')

if __name__ == '__main__':
    app.run(port=8271, debug=False)
