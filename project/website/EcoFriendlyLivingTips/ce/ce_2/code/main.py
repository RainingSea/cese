from flask import Flask, render_template, request, redirect, url_for, session
from DataManager import DataManager
from User import User
from Tip import Tip
from Resource import Resource
from ForumPost import ForumPost

app = Flask(__name__)
app.secret_key = 'your_secret_key'
data_manager = DataManager()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']
    new_user = User(username, password, email)
    data_manager.save_user(new_user)
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    tips = data_manager.load_tips()
    resources = data_manager.load_resources()
    return render_template('dashboard.html', tips=tips, resources=resources)

@app.route('/forum')
def forum():
    posts = data_manager.load_forum_posts()
    return render_template('forum.html', posts=posts)

@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(port=9030, debug=False)
