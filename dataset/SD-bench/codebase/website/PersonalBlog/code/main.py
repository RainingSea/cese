from flask import Flask, render_template, request, redirect, session, url_for
from user import User
from post import Post
from auth import Auth

app = Flask(__name__)
app.secret_key = 'your_secret_key'

auth = Auth()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        if auth.register(username, password, email):
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/main_blog')
def main_blog():
    posts = Post.load_all()
    if not posts:
        return render_template('main_blog.html', posts=[])
    return render_template('main_blog.html', posts=posts)

@app.route('/new_post', methods=['GET', 'POST'])
def new_post():
    if request.method == 'POST':
        username = session.get('username')
        title = request.form['title']
        content = request.form['content']
        post = Post(username, title, content)
        post.save()
        return redirect(url_for('main_blog'))
    return render_template('new_post.html')

@app.route('/view_post/<int:post_id>')
def view_post(post_id):
    posts = Post.load_all()
    if post_id < len(posts):
        return render_template('view_post.html', post=posts[post_id])
    return redirect(url_for('main_blog'))

@app.route('/edit_post/<int:post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    posts = Post.load_all()
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        post = Post(posts[post_id].username, title, content)
        post.save()
        return redirect(url_for('main_blog'))
    if post_id < len(posts):
        return render_template('edit_post.html', post=posts[post_id])
    return redirect(url_for('main_blog'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8311, debug=False)
