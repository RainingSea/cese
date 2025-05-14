from flask import Flask, render_template, redirect, url_for, request, session
from flask_session import Session
import os

app = Flask(__name__)
app.config["SECRET_KEY"] = "your_secret_key"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Import controllers
from auth_controller import AuthController
from profile_controller import ProfileController
from content_controller import ContentController
from interaction_controller import InteractionController

auth = AuthController()
profile = ProfileController()
content = ContentController()
interaction = InteractionController()

@app.route('/')
def home():
    if 'username' in session:
        return redirect(url_for('feed'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if auth.login(username, password):
            session['username'] = username
            return redirect(url_for('feed'))
        return render_template('login.html', error="Invalid credentials")
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if auth.register(username, password):
            return redirect(url_for('login'))
        return render_template('register.html', error="Username already exists")
    return render_template('register.html')

@app.route('/logout')
def logout():
    auth.logout()
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/profile')
def profile_page():
    if 'username' not in session:
        return redirect(url_for('login'))
    username = session['username']
    profile_data = profile.get_profile(username)
    return render_template('profile.html', profile=profile_data)

@app.route('/feed')
def feed():
    if 'username' not in session:
        return redirect(url_for('login'))
    feed_data = content.get_feed()
    return render_template('feed.html', feed=feed_data, username=session['username'])

@app.route('/content/<content_id>')
def content_page(content_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    content_data = content.get_content(content_id)
    return render_template('content.html', content=content_data, username=session['username'])

if __name__ == '__main__':
    app.run(port=8101, debug=False)
