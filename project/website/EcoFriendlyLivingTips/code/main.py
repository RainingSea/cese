from flask import Flask, render_template, request, redirect, session, flash
from user import User
from tip import Tip
from resource import Resource
from forum_post import ForumPost
from eco_friendly_living_tips import EcoFriendlyLivingTips

app = Flask(__name__)
app.secret_key = 'your_secret_key'
eco_friendly_living_tips = EcoFriendlyLivingTips()

@app.route('/', methods=['GET', 'POST'])
def login():
    """Handles user login."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if eco_friendly_living_tips.login_user(username, password):
            session['username'] = username
            return redirect('/dashboard')
        else:
            flash('Invalid username or password. Please try again.')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Handles user registration."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        eco_friendly_living_tips.register_user(username, password, email)
        flash('Registration successful! You can now log in.')
        return redirect('/')
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    """Displays the user dashboard with tips and resources."""
    tips = eco_friendly_living_tips.tips
    resources = eco_friendly_living_tips.resources
    return render_template('dashboard.html', tips=tips, resources=resources)

@app.route('/tips', methods=['GET', 'POST'])
def tips():
    """Handles tip submission and displays existing tips."""
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        eco_friendly_living_tips.submit_tip(title, content)
        flash('Tip submitted successfully!')
        return redirect('/tips')
    tips = eco_friendly_living_tips.tips
    return render_template('tips.html', tips=tips)

@app.route('/submit_resource', methods=['POST'])
def submit_resource():
    """Handles resource submission."""
    title = request.form['title']
    url = request.form['url']
    eco_friendly_living_tips.submit_resource(title, url)
    flash('Resource submitted successfully!')
    return redirect('/dashboard')

@app.route('/forum', methods=['GET', 'POST'])
def forum():
    """Handles forum post submission and displays existing posts."""
    if request.method == 'POST':
        username = session.get('username')
        content = request.form['content']
        eco_friendly_living_tips.submit_forum_post(username, content)
        flash('Post submitted successfully!')
        return redirect('/forum')
    forum_posts = eco_friendly_living_tips.forum_posts
    return render_template('forum.html', forum_posts=forum_posts)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    """Handles contact form submission."""
    if request.method == 'POST':
        flash('Your message has been sent successfully!')
    return render_template('contact.html')

@app.route('/logout')
def logout():
    """Handles user logout."""
    session.pop('username', None)
    flash('You have been logged out.')
    return redirect('/')

if __name__ == '__main__':
    eco_friendly_living_tips.load_data()
    app.run(port=9033, debug=False)
