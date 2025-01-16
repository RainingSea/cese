from flask import Flask, render_template, request, redirect, session
from user_manager import UserManager
from album_manager import AlbumManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'
user_manager = UserManager()
album_manager = AlbumManager()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            return redirect('/')
        else:
            return "Username already exists!"
    return render_template('registration.html')

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    if user_manager.login(username, password):
        session['username'] = username
        return redirect('/albums')
    return "Login failed!"

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')

@app.route('/albums')
def albums():
    if 'username' in session:
        return render_template('album_exploration.html', albums=album_manager.get_albums())
    return redirect('/')

@app.route('/create_album', methods=['GET', 'POST'])
def create_album():
    if request.method == 'POST':
        title = request.form['title']
        owner = session['username']
        images = request.form.getlist('images')
        is_private = 'is_private' in request.form
        album_manager.create_album(title, owner, images, is_private)
        return redirect('/albums')
    return render_template('album_creation.html')

@app.route('/explore')
def explore():
    if 'username' in session:
        albums = album_manager.explore_albums()
        return render_template('explore.html', albums=albums)
    return redirect('/')

@app.route('/share_album', methods=['POST'])
def share_album():
    if 'username' in session:
        album_id = request.form['album_id']
        shared_with = request.form.getlist('shared_with')
        album_manager.share_album(album_id, shared_with)
        return redirect('/albums')
    return redirect('/')

@app.route('/shared_albums')
def shared_albums():
    if 'username' in session:
        shared_albums = user_manager.get_shared_albums(session['username'])
        return render_template('shared_albums.html', albums=shared_albums)
    return redirect('/')

@app.route('/follow_user', methods=['POST'])
def follow_user():
    if 'username' in session:
        followee = request.form['followee']
        user_manager.follow_user(session['username'], followee)
        return redirect('/albums')
    return redirect('/')

@app.route('/followers')
def followers():
    if 'username' in session:
        followers = user_manager.get_followers(session['username'])
        return render_template('followers.html', followers=followers)
    return redirect('/')

@app.route('/notifications')
def notifications():
    if 'username' in session:
        notifications = album_manager.user_manager.data_manager.load_notifications(session['username'])
        return render_template('notifications.html', notifications=notifications)
    return redirect('/')

if __name__ == '__main__':
    app.run(port=8658, debug=False)
