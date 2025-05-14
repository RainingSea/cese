from flask import Flask, render_template, redirect, request, session, flash
import json
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'secret_key'

class UserManager:
    def __init__(self, users_file='users.txt'):
        self.users_file = users_file
        if not os.path.exists(users_file):
            open(users_file, 'w').close()

    def register(self, username, password):
        with open(self.users_file, 'r') as f:
            for line in f:
                if line.startswith(username + '|'):
                    return False
        with open(self.users_file, 'a') as f:
            f.write(f"{username}|{password}\n")
        return True

    def login(self, username, password):
        with open(self.users_file, 'r') as f:
            for line in f:
                parts = line.strip().split('|')
                if parts[0] == username and parts[1] == password:
                    return True
        return False

class ProfileManager:
    def __init__(self, profiles_file='profiles.txt'):
        self.profiles_file = profiles_file
        if not os.path.exists(profiles_file):
            open(profiles_file, 'w').close()

    def get_profile(self, username):
        with open(self.profiles_file, 'r') as f:
            for line in f:
                profile = json.loads(line.strip())
                if profile['username'] == username:
                    return profile
        return {'username': username, 'bio': ''}

    def update_profile(self, username, data):
        profiles = []
        found = False
        if os.path.exists(self.profiles_file):
            with open(self.profiles_file, 'r') as f:
                for line in f:
                    profile = json.loads(line.strip())
                    if profile['username'] == username:
                        profile.update(data)
                        found = True
                    profiles.append(profile)
        
        if not found:
            profiles.append({'username': username, **data})

        with open(self.profiles_file, 'w') as f:
            for profile in profiles:
                f.write(json.dumps(profile) + '\n')
        return True

class ContentManager:
    def __init__(self, posts_file='posts.txt'):
        self.posts_file = posts_file
        if not os.path.exists(posts_file):
            open(posts_file, 'w').close()

    def create_post(self, author, content):
        post = {
            'author': author,
            'content': content,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        with open(self.posts_file, 'a') as f:
            f.write(json.dumps(post) + '\n')
        return True

    def get_feed(self):
        posts = []
        if os.path.exists(self.posts_file):
            with open(self.posts_file, 'r') as f:
                for line in f:
                    posts.append(json.loads(line.strip()))
        return posts[::-1]

    def get_user_posts(self, username):
        posts = []
        if os.path.exists(self.posts_file):
            with open(self.posts_file, 'r') as f:
                for line in f:
                    post = json.loads(line.strip())
                    if post['author'] == username:
                        posts.append(post)
        return posts[::-1]

class InteractionManager:
    def __init__(self, interactions_file='interactions.txt'):
        self.interactions_file = interactions_file
        if not os.path.exists(interactions_file):
            open(interactions_file, 'w').close()

    def like_post(self, user, post_id):
        with open(self.interactions_file, 'a') as f:
            f.write(f"{post_id}|{user}|like\n")
        return True

    def comment(self, user, post_id, text):
        with open(self.interactions_file, 'a') as f:
            f.write(f"{post_id}|{user}|comment|{text}\n")
        return True

user_manager = UserManager()
profile_manager = ProfileManager()
content_manager = ContentManager()
interaction_manager = InteractionManager()

@app.route('/')
def home():
    if 'username' in session:
        return redirect('/feed')
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.login(username, password):
            session['username'] = username
            return redirect('/feed')
        flash('Invalid username or password')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            session['username'] = username
            return redirect('/profile')
        flash('Username already exists')
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/login')

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'username' not in session:
        return redirect('/login')
    
    username = session['username']
    if request.method == 'POST':
        bio = request.form['bio']
        profile_manager.update_profile(username, {'bio': bio})
    
    profile = profile_manager.get_profile(username)
    posts = content_manager.get_user_posts(username)
    return render_template('profile.html', profile=profile, posts=posts, current_user=username)

@app.route('/feed')
def feed():
    if 'username' not in session:
        return redirect('/login')
    posts = content_manager.get_feed()
    return render_template('feed.html', posts=posts, current_user=session['username'])

@app.route('/create_post', methods=['GET', 'POST'])
def create_post():
    if 'username' not in session:
        return redirect('/login')
    
    if request.method == 'POST':
        content = request.form['content']
        content_manager.create_post(session['username'], content)
        return redirect('/feed')
    
    return render_template('create_post.html', current_user=session['username'])

if __name__ == '__main__':
    app.run(port=8103, debug=False)
