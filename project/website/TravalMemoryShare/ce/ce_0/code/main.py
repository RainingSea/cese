from flask import Flask, render_template, request, redirect, url_for, session
from DataManager import DataManager
from User import User
from Album import Album
from Comment import Comment

app = Flask(__name__)
app.secret_key = 'your_secret_key'
data_manager = DataManager()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User(username, password)
        data_manager.save_user(user)
        return redirect(url_for('login'))
    return render_template('registration.html')

@app.route('/explore')
def explore():
    albums = data_manager.load_albums()
    return render_template('explore.html', albums=albums)

@app.route('/create_album', methods=['GET', 'POST'])
def create_album():
    if request.method == 'POST':
        title = request.form['title']
        user = session.get('username')
        images = request.form.getlist('images')
        is_public = 'is_public' in request.form
        album = Album(title, user, images, is_public)
        data_manager.save_album(album)
        return redirect(url_for('explore'))
    return render_template('album_creation.html')

if __name__ == '__main__':
    app.run(port=8653, debug=False)
