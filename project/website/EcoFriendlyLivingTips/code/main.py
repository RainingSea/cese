from flask import Flask, render_template, request, redirect, session
from flask_session import Session
from UserManager import UserManager
from TipManager import TipManager
from ResourceManager import ResourceManager
from ForumManager import ForumManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

user_manager = UserManager()
tip_manager = TipManager()
resource_manager = ResourceManager()
forum_manager = ForumManager()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.login(username, password):
            session['username'] = username
            return redirect('/dashboard')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        if user_manager.register(username, password, email):
            return redirect('/')
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect('/')
    tips = tip_manager.get_tips()
    resources = resource_manager.get_resources()
    return render_template('dashboard.html', tips=tips, resources=resources)

@app.route('/introduction')
def introduction():
    return render_template('introduction.html')

@app.route('/tips', methods=['GET', 'POST'])
def tips():
    if request.method == 'POST':
        tip = request.form['tip']
        tip_manager.submit_tip(tip)
        return redirect('/tips')
    tips = tip_manager.get_tips()
    return render_template('tips.html', tips=tips)

@app.route('/resources', methods=['GET', 'POST'])
def resources():
    if request.method == 'POST':
        title = request.form['title']
        url = request.form['url']
        resource_manager.add_resource(title, url)
        return redirect('/resources')
    resources = resource_manager.get_resources()
    return render_template('resources.html', resources=resources)

@app.route('/forum', methods=['GET', 'POST'])
def forum():
    if request.method == 'POST':
        post = request.form['post']
        forum_manager.add_post(post)
        return redirect('/forum')
    posts = forum_manager.get_posts()
    return render_template('forum.html', posts=posts)

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'username' not in session:
        return redirect('/')
    user_info = next((user for user in user_manager.users if user['username'] == session['username']), None)
    if request.method == 'POST':
        new_info = {
            'username': request.form['username'],
            'email': request.form['email']
        }
        user_manager.update_profile(session['username'], new_info)
        return redirect('/profile')
    return render_template('profile.html', user=user_info)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        # Handle contact form submission (e.g., save to a file or send an email)
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(port=8330, debug=False)
