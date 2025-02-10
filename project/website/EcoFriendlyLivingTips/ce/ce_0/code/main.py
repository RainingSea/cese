from flask import Flask, render_template, request, redirect, url_for, session
from user import User
from tip import Tip
from resource import Resource
from forum_post import ForumPost

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    tips = Tip().load_tips()
    resources = Resource().load_resources()
    return render_template('dashboard.html', tips=tips, resources=resources)

@app.route('/tips', methods=['GET', 'POST'])
def tips_page():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        tip = Tip(title, description)
        tip.save()
        return redirect(url_for('tips_page'))
    return render_template('tips.html')

@app.route('/resources', methods=['GET', 'POST'])
def resources_page():
    if request.method == 'POST':
        url = request.form['url']
        description = request.form['description']
        resource = Resource(url, description)
        resource.save()
        return redirect(url_for('resources_page'))
    return render_template('resources.html')

@app.route('/forum', methods=['GET', 'POST'])
def forum_page():
    if request.method == 'POST':
        username = session.get('username', 'Guest')
        content = request.form['content']
        post = ForumPost(username, content)
        post.save()
        return redirect(url_for('forum_page'))
    posts = ForumPost().load_posts()
    return render_template('forum.html', posts=posts)

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(port=8623, debug=False)
