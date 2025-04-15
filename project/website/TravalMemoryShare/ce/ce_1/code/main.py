from flask import Flask, render_template, request, redirect, url_for, flash, session
from user import User
from album import Album
from interaction import Interaction

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a random secret key

class Application:
    def __init__(self):
        self.users = User.load_users()
        self.albums = Album.load_albums()
        self.interactions = Interaction.load_interactions()

    def register_user(self, username: str, password: str) -> bool:
        for user in self.users:
            if user.username == username:
                return False  # Username already exists
        new_user = User(username, password)
        new_user.save()
        self.users.append(new_user)
        return True

    def login_user(self, username: str, password: str) -> bool:
        for user in self.users:
            if user.username == username and user.password == password:
                session['username'] = username  # Store username in session
                return True  # Login successful
        return False  # Invalid credentials

    def logout_user(self):
        session.pop('username', None)  # Remove username from session

@app.route('/', methods=['GET', 'POST'])
def login():
    app_instance = Application()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if app_instance.login_user(username, password):
            flash('Login successful!', 'success')
            return redirect(url_for('album_gallery'))
        else:
            flash('Invalid credentials. Please try again.', 'danger')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    app_instance = Application()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if app_instance.register_user(username, password):
            flash('Registration successful! You can now log in.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Username already exists. Please choose another one.', 'danger')
    return render_template('registration.html')

@app.route('/album_gallery')
def album_gallery():
    app_instance = Application()
    return render_template('album_gallery.html', albums=app_instance.albums)

@app.route('/logout')
def logout():
    app_instance = Application()
    app_instance.logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8324, debug=False)
