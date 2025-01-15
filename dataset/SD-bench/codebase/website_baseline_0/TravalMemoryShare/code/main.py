from flask import Flask, render_template, request, redirect, url_for, session, flash
from user import User
from album import Album
from comment import Comment

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def load_users():
    users = {}
    with open('users.txt', 'r') as file:
        for line in file:
            username, password = line.strip().split('|')
            users[username] = password
    return users

def load_albums():
    albums = []
    with open('albums.txt', 'r') as file:
        for line in file:
            title, photos, is_public = line.strip().split('|')
            albums.append(Album(title, photos.split(','), is_public == 'True'))
    return albums

def load_comments():
    comments = []
    with open('comments.txt', 'r') as file:
        for line in file:
            user, album_id, content = line.strip().split('|')
            comments.append(Comment(user, album_id, content))
    return comments

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
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Registration failed. Username may already exist.', 'error')
    return render_template('registration.html')

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    user = User(username, password)
    if user.login():
        session['username'] = username
        return redirect(url_for('album'))
    flash('Login failed. Please check your credentials.', 'error')
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

@app.route('/album', methods=['GET', 'POST'])
def album():
    if request.method == 'POST':
        title = request.form['title']
        photos = request.form.getlist('photos')
        is_public = 'is_public' in request.form
        album = Album(title, photos, is_public)
        album.create_album()
        flash('Album created successfully!', 'success')
        return redirect(url_for('album'))
    albums = load_albums()
    return render_template('album.html', albums=albums)

@app.route('/customize_album/<album_title>', methods=['GET', 'POST'])
def customize_album(album_title):
    if request.method == 'POST':
        # Customization logic can be implemented here
        flash('Album layout customized successfully!', 'success')
        return redirect(url_for('album'))
    return render_template('customize_album.html', album_title=album_title)

@app.route('/share_album/<album_title>', methods=['GET'])
def share_album(album_title):
    # Sharing logic can be implemented here
    flash(f'Album "{album_title}" shared successfully!', 'success')
    return redirect(url_for('album'))

@app.route('/explore_albums', methods=['GET'])
def explore_albums():
    albums = load_albums()
    return render_template('explore_albums.html', albums=albums)

@app.route('/follow_user/<username>', methods=['POST'])
def follow_user(username):
    # Follow user logic can be implemented here
    flash(f'You are now following {username}!', 'success')
    return redirect(url_for('explore_albums'))

@app.route('/interact_with_user/<username>', methods=['POST'])
def interact_with_user(username):
    # Interaction logic can be implemented here
    flash(f'You interacted with {username}!', 'success')
    return redirect(url_for('explore_albums'))

if __name__ == '__main__':
    app.run(port=8557, debug=False)
