from flask import Flask, render_template, request, redirect, url_for
from tools import SearchEngine, UserProfile, Bookmark, Feedback

app = Flask(__name__)

# Load user profiles from file
def load_user_profiles():
    profiles = {}
    with open('users.txt', 'r') as file:
        for line in file:
            username, password = line.strip().split('|')
            profiles[username] = {'password': password, 'preferences': {}}
    return profiles

user_profiles = load_user_profiles()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in user_profiles and user_profiles[username]['password'] == password:
            return redirect(url_for('home', username=username))
    return render_template('login.html')

@app.route('/home/<username>')
def home(username):
    return f"Welcome {username}!"

if __name__ == '__main__':
    app.run(port=8177, debug=False)
