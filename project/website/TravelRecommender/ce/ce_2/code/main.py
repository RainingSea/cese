from flask import Flask, render_template, request, redirect, url_for, session
from auth import AuthManager
from recommendations import RecommendationEngine

app = Flask(__name__)
app.secret_key = 'secret_key'

auth_manager = AuthManager()
recommendation_engine = RecommendationEngine()

@app.route('/')
def home():
    if auth_manager.is_logged_in():
        return redirect(url_for('recommendations'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if auth_manager.login(username, password):
            return redirect(url_for('recommendations'))
        return render_template('login.html', error='Invalid credentials')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if auth_manager.register(username, password):
            return redirect(url_for('login'))
        return render_template('register.html', error='Username already exists')
    return render_template('register.html')

@app.route('/logout')
def logout():
    auth_manager.logout()
    return redirect(url_for('login'))

@app.route('/recommendations')
def recommendations():
    if not auth_manager.is_logged_in():
        return redirect(url_for('login'))
    username = session['username']
    # In a complete implementation, we would get user preferences first
    recommendations = recommendation_engine.get_recommendations({})
    return render_template('recommendations.html', recommendations=recommendations)

if __name__ == '__main__':
    app.run(port=8073, debug=False)
