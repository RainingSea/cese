from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO
from user_manager import UserManager
from content_manager import ContentManager

app = Flask(__name__)
socketio = SocketIO(app)

user_manager = UserManager()
content_manager = ContentManager()

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

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if request.method == 'POST':
        username = request.form['username']
        bio = request.form['bio']
        user_manager.updateProfile(username, bio)
    return render_template('profile.html')

@app.route('/feed')
def feed():
    articles = content_manager.getFeed()
    return render_template('feed.html', articles=articles)

if __name__ == '__main__':
    socketio.run(app)