from flask import Flask, render_template, request, redirect, url_for, session
import json
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

class UserManager:
    def __init__(self, users_file='users.txt'):
        self.users_file = users_file

    def register(self, username, password):
        with open(self.users_file, 'a') as f:
            f.write(f"{username}|{password}\n")
        return True

    def login(self, username, password):
        with open(self.users_file, 'r') as f:
            for line in f:
                stored_username, stored_password = line.strip().split('|')
                if stored_username == username and stored_password == password:
                    return True
        return False

class ProfileManager:
    def __init__(self, profiles_file='profiles.txt'):
        self.profiles_file = profiles_file

    def get_profile(self, username):
        with open(self.profiles_file, 'r') as f:
            for line in f:
                profile = json.loads(line.strip())
                if profile['username'] == username:
                    return profile
        return {'username': username, 'bio': '', 'info': ''}

    def update_profile(self, username, bio, info):
        profile = {'username': username, 'bio': bio, 'info': info}
        with open(self.profiles_file, 'a') as f:
            f.write(json.dumps(profile) + '\n')
        return True

class ContentManager:
    def __init__(self, content_file='content.txt'):
        self.content_file = content_file

    def upload_content(self, username, title, content):
        post = {
            'username': username,
            'title': title,
            'content': content,
            'timestamp': str(datetime.now())
        }
        with open(self.content_file, 'a') as f:
            f.write(json.dumps(post) + '\n')
        return True

    def get_feed(self, username):
        feed = []
        with open(self.content_file, 'r') as f:
            for line in f:
                post = json.loads(line.strip())
                feed.append(post)
        return feed[::-1]  # Return in reverse chronological order

class InteractionManager:
    def __init__(self, interactions_file='interactions.txt'):
        self.interactions_file = interactions_file

    def like_content(self, user, content_id):
        interaction = {
            'type': 'like',
            'user': user,
            'content_id': content_id,
            'timestamp': str(datetime.now())
        }
        with open(self.interactions_file, 'a') as f:
            f.write(json.dumps(interaction) + '\n')
        return True

    def comment(self, user, content_id, text):
        interaction = {
            'type': 'comment',
            'user': user,
            'content_id': content_id,
            'text': text,
            'timestamp': str(datetime.now())
        }
        with open(self.interactions_file, 'a') as f:
            f.write(json.dumps(interaction) + '\n')
        return True

    def follow(self, user, target_user):
        interaction = {
            'type': 'follow',
            'user': user,
            'target_user': target_user,
            'timestamp': str(datetime.now())
        }
        with open(self.interactions_file, 'a') as f:
            f.write(json.dumps(interaction) + '\n')
        return True

user_manager = UserManager()
profile_manager = ProfileManager()
content_manager = ContentManager()
interaction_manager = InteractionManager()

@app.route('/')
def home():
    if 'username' not in session:
        return redirect(url_for('login'))
    return redirect(url_for('feed'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_manager.register(username, password)
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.login(username, password):
            session['username'] = username
            return redirect(url_for('feed'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    username = session['username']
    if request.method == 'POST':
        bio = request.form['bio']
        info = request.form['info']
        profile_manager.update_profile(username, bio, info)
    
    profile = profile_manager.get_profile(username)
    return render_template('profile.html', profile=profile)

@app.route('/feed')
def feed():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    username = session['username']
    feed = content_manager.get_feed(username)
    return render_template('feed.html', feed=feed, username=username)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        content_manager.upload_content(session['username'], title, content)
        return redirect(url_for('feed'))
    return render_template('upload.html')

if __name__ == '__main__':
    app.run(port=8099, debug=False)
