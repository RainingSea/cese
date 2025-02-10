from flask import Flask, render_template, request, redirect, session
from data_manager import DataManager
from models import User, Tip, Resource, ForumPost

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
        users = data_manager.load_users()
        users.append(User(username, password))
        data_manager.save_users(users)
        return redirect('/')
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/tips', methods=['GET', 'POST'])
def tips():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        tips = data_manager.load_tips()
        tips.append(Tip(title, content))
        data_manager.save_tips(tips)
        return redirect('/tips')
    tips = data_manager.load_tips()
    return render_template('tips.html', tips=tips)

@app.route('/resources', methods=['GET', 'POST'])
def resources():
    if request.method == 'POST':
        title = request.form['title']
        link = request.form['link']
        resources = data_manager.load_resources()
        resources.append(Resource(title, link))
        data_manager.save_resources(resources)
        return redirect('/resources')
    resources = data_manager.load_resources()
    return render_template('resources.html', resources=resources)

@app.route('/forum', methods=['GET', 'POST'])
def forum():
    if request.method == 'POST':
        username = session.get('username')
        content = request.form['content']
        posts = data_manager.load_forum_posts()
        posts.append(ForumPost(username, content))
        data_manager.save_forum_posts(posts)
        return redirect('/forum')
    posts = data_manager.load_forum_posts()
    return render_template('forum.html', posts=posts)

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(port=8626, debug=False)
