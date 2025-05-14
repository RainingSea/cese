from flask import Flask, render_template, request, redirect, url_for, session, flash
from managers import UserManager, ProfileManager, ContentManager, InteractionManager
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'secret_key'

user_manager = UserManager()
profile_manager = ProfileManager()
content_manager = ContentManager()
interaction_manager = InteractionManager()

# Initialize data files if they don't exist
for filename in ['users.txt', 'profiles.txt', 'content.txt', 'interactions.txt', 'followers.txt']:
    if not os.path.exists(filename):
        open(filename, 'w').close()

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
        if user_manager.login(username, password):
            session['username'] = username
            flash('Login successful!', 'success')
            return redirect(url_for('feed'))
        flash('Invalid username or password', 'error')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.user_exists(username):
            flash('Username already exists', 'error')
        elif user_manager.register(username, password):
            profile_manager.create_profile(username, '')
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Registration failed', 'error')
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('Logged out successfully', 'success')
    return redirect(url_for('login'))

@app.route('/profile/<username>')
def view_profile(username):
    if 'username' not in session:
        return redirect(url_for('login'))
    
    profile_data = profile_manager.get_profile(username)
    user_content = content_manager.get_content_by_user(username)
    is_following = interaction_manager.check_following(session['username'], username)
    
    return render_template('profile.html', 
                         username=username,
                         current_user=session['username'],
                         bio=profile_data['bio'] if profile_data else '',
                         posts=user_content,
                         is_following=is_following)

@app.route('/follow', methods=['POST'])
def follow():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    target_user = request.form['target_user']
    interaction_manager.follow_user(session['username'], target_user)
    return redirect(url_for('view_profile', username=target_user))

@app.route('/unfollow', methods=['POST'])
def unfollow():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    target_user = request.form['target_user']
    interaction_manager.unfollow_user(session['username'], target_user)
    return redirect(url_for('view_profile', username=target_user))

@app.route('/feed')
def feed():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    username = session['username']
    following = interaction_manager.get_following(username)
    feed_content = content_manager.get_feed_for_users([username] + following)
    
    feed_data = []
    for content in feed_content:
        content_id = content['id']
        interactions = interaction_manager.get_interactions(content_id)
        feed_data.append({
            'content': content,
            'likes': len([i for i in interactions if i['type'] == 'like']),
            'comments': [i for i in interactions if i['type'] == 'comment']
        })
    
    return render_template('feed.html', 
                         username=username,
                         feed=feed_data)

@app.route('/like', methods=['POST'])
def like():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    content_id = request.form['content_id']
    interaction_manager.like_content(session['username'], content_id)
    return redirect(url_for('feed'))

@app.route('/comment', methods=['POST'])
def comment():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    content_id = request.form['content_id']
    text = request.form['text']
    interaction_manager.comment(session['username'], content_id, text)
    return redirect(url_for('feed'))

if __name__ == '__main__':
    app.run(port=8106, debug=False)
