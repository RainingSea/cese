from flask import Flask, render_template, request, redirect, session, flash
from user_manager import UserManager
from content_manager import ContentManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'

user_manager = UserManager()
content_manager = ContentManager()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.login(username, password):
            session['username'] = username
            return redirect('/feed')
        else:
            flash('Invalid credentials. Please try again.')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            flash('Registration successful! Please log in.')
            return redirect('/')
        else:
            flash('Username already taken. Please choose another.')
    return render_template('register.html')

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'username' not in session:
        return redirect('/')
    if request.method == 'POST':
        bio = request.form['bio']
        user_manager.update_profile(session['username'], bio)
        flash('Profile updated successfully!')
    bio = user_manager.profiles.get(session['username'], '')
    return render_template('profile.html', bio=bio)

@app.route('/feed')
def feed():
    if 'username' not in session:
        return redirect('/')
    articles = content_manager.get_feed()
    return render_template('feed.html', articles=articles)

@app.route('/share', methods=['POST'])
def share_article():
    if 'username' not in session:
        return redirect('/')
    article = request.form['article']
    content_manager.share_article(session['username'], article)
    flash('Article shared successfully!')
    return redirect('/feed')

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out.')
    return redirect('/')

if __name__ == '__main__':
    app.run(port=8421, debug=False)
