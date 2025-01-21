from flask import Flask, render_template, request, redirect, url_for, session
from user import User
from post import Post
from blog_app import BlogApp

app = Flask(__name__)
app.secret_key = 'your_secret_key'
blog_app = BlogApp()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        message = blog_app.register(username, password, email)
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/main', methods=['GET'])
def main():
    if 'username' not in session:
        return redirect(url_for('login'))
    posts = blog_app.get_posts(session['username'])
    return render_template('main.html', posts=posts)

@app.route('/new_post', methods=['GET', 'POST'])
def new_post():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        blog_app.create_post(title, content, session['username'])
        return redirect(url_for('main'))
    return render_template('new_post.html')

@app.route('/view_post/<int:post_id>', methods=['GET'])
def view_post(post_id):
    post = blog_app.posts[post_id]
    return render_template('view_post.html', post=post)

@app.route('/edit_post/<int:post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        blog_app.edit_post(post_id, title, content)
        return redirect(url_for('main'))
    post = blog_app.posts[post_id]
    return render_template('edit_post.html', post=post)

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    message = blog_app.login(username, password)
    if message == "Login successful":
        session['username'] = username
        return redirect(url_for('main'))
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8976, debug=False)
