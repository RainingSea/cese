from flask import Flask, render_template, request, redirect, url_for
from user import User
from profile import Profile
from study_group import StudyGroup
from resource import Resource
from message import Message
from data_storage import DataStorage
import time
import logging

app = Flask(__name__)
data_storage = DataStorage()
logging.basicConfig(level=logging.INFO)

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User(username, password)
        if user.register():
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if request.method == 'POST':
        username = request.form['username']
        interests = request.form.getlist('interests')
        profile = Profile(username, interests)
        profile.update_profile(interests)
    return render_template('profile.html')

@app.route('/groups')
def groups():
    study_groups = data_storage.load_groups()
    return render_template('groups.html', groups=study_groups)

@app.route('/resources')
def resources():
    educational_resources = data_storage.load_resources()
    return render_template('resources.html', resources=educational_resources)

if __name__ == '__main__':
    app.run(port=8553, debug=False)
    time.sleep(2)  # Allow time for the server to fully initialize